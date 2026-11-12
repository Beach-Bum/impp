"""Verification certificate generation, signing, and validation."""

import json
import uuid
import base64
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone, timedelta
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization

from ..config import CERTIFICATE_EXPIRY_DAYS, CERTS_DIR, CRL_PATH


@dataclass
class VerificationCertificate:
    """A verification certificate for a memory artifact."""

    id: str
    version: str
    artifact_hash: str
    benchmark: dict  # {id, domain, protocol_count, held_out_count, hash}
    results: dict  # {buyer_avg_error, novice_avg_error, transfer_efficiency_pct, ...}
    adversarial: dict  # {aggregate_score, bias_score, ..., verdict}
    trust_score: float
    issued_at: str
    expires_at: str
    referee_model: str
    signature: str = ""
    # Full-coverage integrity digest of the verified artifact
    # (MemoryArtifact.compute_integrity). Being part of the signed payload,
    # it binds the signature to every field of the artifact, not only to the
    # four fields behind artifact_hash. Empty on certificates issued before
    # the digest existed.
    artifact_integrity: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        # Omitted when empty so that certificates issued before the digest
        # existed serialize, and therefore sign and verify, exactly as before.
        if not d.get("artifact_integrity"):
            d.pop("artifact_integrity", None)
        return d

    def matches_artifact(self, artifact) -> bool:
        """Check that ``artifact`` is the one this certificate was issued for.

        Compares the content address and, when the certificate carries an
        integrity digest, the digest recomputed over the whole artifact, so a
        change to any field (e.g. the attestation) is detected. For
        certificates without a digest only the content address is compared.
        """
        if artifact.hash != self.artifact_hash:
            return False
        if artifact.hash != artifact.compute_hash():
            return False
        if self.artifact_integrity:
            return artifact.compute_integrity() == self.artifact_integrity
        return True

    def _signable_payload(self) -> bytes:
        """Canonical JSON bytes for signing (excludes signature field)."""
        d = self.to_dict()
        d.pop("signature", None)
        return json.dumps(d, sort_keys=True, separators=(",", ":")).encode()

    def sign(self, private_key: Ed25519PrivateKey) -> None:
        """Sign this certificate in place with an Ed25519 private key."""
        sig = private_key.sign(self._signable_payload())
        self.signature = base64.b64encode(sig).decode()

    def verify_signature(self, public_key: Ed25519PublicKey) -> bool:
        """Verify this certificate's signature against a public key."""
        if not self.signature:
            return False
        try:
            sig_bytes = base64.b64decode(self.signature)
            public_key.verify(sig_bytes, self._signable_payload())
            return True
        except Exception:
            return False

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def is_expired(self) -> bool:
        expiry = datetime.fromisoformat(self.expires_at)
        return datetime.now(timezone.utc) > expiry

    @classmethod
    def from_dict(cls, data: dict) -> "VerificationCertificate":
        return cls(**data)

    @classmethod
    def from_json(cls, text: str) -> "VerificationCertificate":
        return cls.from_dict(json.loads(text))


def generate_keypair(key_dir: Path | None = None) -> tuple[Path, Path]:
    """Generate an Ed25519 keypair and save to disk.

    Returns:
        Tuple of (private_key_path, public_key_path).
    """
    key_dir = key_dir or CERTS_DIR
    key_dir.mkdir(parents=True, exist_ok=True)

    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    priv_path = key_dir / "impp_signing.key"
    pub_path = key_dir / "impp_signing.pub"

    priv_path.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    priv_path.chmod(0o600)

    pub_path.write_bytes(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )

    return priv_path, pub_path


def load_private_key(path: Path | None = None) -> Ed25519PrivateKey:
    """Load an Ed25519 private key from PEM file."""
    path = path or (CERTS_DIR / "impp_signing.key")
    key = serialization.load_pem_private_key(path.read_bytes(), password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise TypeError(f"Expected Ed25519 private key, got {type(key)}")
    return key


def load_public_key(path: Path | None = None) -> Ed25519PublicKey:
    """Load an Ed25519 public key from PEM file."""
    path = path or (CERTS_DIR / "impp_signing.pub")
    key = serialization.load_pem_public_key(path.read_bytes())
    if not isinstance(key, Ed25519PublicKey):
        raise TypeError(f"Expected Ed25519 public key, got {type(key)}")
    return key


def generate_certificate(
    artifact_hash: str,
    benchmark_info: dict,
    results: dict,
    adversarial: dict,
    trust_score: float,
    referee_model: str,
    expiry_days: int = CERTIFICATE_EXPIRY_DAYS,
    signing_key: Ed25519PrivateKey | None = None,
    artifact_integrity: str = "",
) -> VerificationCertificate:
    """Generate a verification certificate, optionally signed.

    Args:
        artifact_hash: Hash of the verified artifact
        benchmark_info: Benchmark metadata
        results: Evaluation results (metrics, per_protocol)
        adversarial: Adversarial probe results
        trust_score: Computed trust score
        referee_model: Model used for verification
        expiry_days: Days until certificate expires
        signing_key: Ed25519 private key for signing (auto-loads from CERTS_DIR if None)
        artifact_integrity: Full-coverage integrity digest of the artifact
            (MemoryArtifact.compute_integrity()); included in the signed payload

    Returns:
        A VerificationCertificate (signed if a key is available).
    """
    now = datetime.now(timezone.utc)

    cert = VerificationCertificate(
        id=str(uuid.uuid4()),
        version="0.1.0",
        artifact_hash=artifact_hash,
        benchmark=benchmark_info,
        results=results,
        adversarial={
            "aggregate_score": adversarial["aggregate_score"],
            "bias_score": adversarial["bias_score"],
            "consistency_score": adversarial["consistency_score"],
            "stego_score": adversarial["stego_score"],
            "overfit_score": adversarial["overfit_score"],
            "verdict": adversarial["verdict"],
            "flags": adversarial.get("all_flags", []),
        },
        trust_score=round(trust_score, 1),
        issued_at=now.isoformat(),
        expires_at=(now + timedelta(days=expiry_days)).isoformat(),
        referee_model=referee_model,
        artifact_integrity=artifact_integrity,
    )

    # Auto-sign if key provided or available on disk
    if signing_key is None:
        try:
            signing_key = load_private_key()
        except (FileNotFoundError, TypeError):
            pass
    if signing_key is not None:
        cert.sign(signing_key)

    return cert


# ── Certificate Revocation List (CRL) ─────────────────────────────────


def load_crl(path: Path | None = None) -> list[dict]:
    """Load the Certificate Revocation List."""
    path = path or CRL_PATH
    if not path.exists():
        return []
    return json.loads(path.read_text())


def save_crl(entries: list[dict], path: Path | None = None) -> None:
    """Save the Certificate Revocation List."""
    path = path or CRL_PATH
    path.write_text(json.dumps(entries, indent=2))


def revoke_certificate(
    cert_id: str,
    reason: str = "publisher_request",
    crl_path: Path | None = None,
) -> dict:
    """Add a certificate to the revocation list.

    Returns the CRL entry.
    """
    entry = {
        "cert_id": cert_id,
        "revoked_at": datetime.now(timezone.utc).isoformat(),
        "reason": reason,
    }
    crl = load_crl(crl_path)
    crl.append(entry)
    save_crl(crl, crl_path)
    return entry


def check_revocation(cert_id: str, crl_path: Path | None = None) -> bool:
    """Check if a certificate has been revoked. Returns True if revoked."""
    crl = load_crl(crl_path)
    return any(entry["cert_id"] == cert_id for entry in crl)
