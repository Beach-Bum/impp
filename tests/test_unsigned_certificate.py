"""Tests that an unsigned certificate is explicit, not silent."""

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

import amm.verification.certificate as certificate_module
from amm.verification.certificate import (
    UnsignedCertificateError,
    VerificationCertificate,
    generate_certificate,
    generate_keypair,
    verify_certificate,
)

ADVERSARIAL = {
    "aggregate_score": 15.0,
    "bias_score": 10.0,
    "consistency_score": 20.0,
    "stego_score": 15.0,
    "overfit_score": 10.0,
    "verdict": "PASS",
    "all_flags": [],
}


def issue(**kwargs):
    return generate_certificate(
        artifact_hash="abc123def456",
        benchmark_info={"id": "bench-1", "domain": "defi"},
        results={"transfer_efficiency_pct": 85.0},
        adversarial=ADVERSARIAL,
        trust_score=82.5,
        referee_model="test-model",
        **kwargs,
    )


@pytest.fixture
def no_key_on_disk(tmp_path, monkeypatch):
    """Point the default key location at an empty directory."""
    monkeypatch.setattr(certificate_module, "CERTS_DIR", tmp_path / "certs")
    return tmp_path / "certs"


def test_default_still_returns_unsigned_certificate(no_key_on_disk):
    """Existing callers are unaffected: no key, no error, no signature."""
    cert = issue()
    assert cert.signature == ""
    assert cert.signed is False


def test_require_signature_raises_without_key(no_key_on_disk):
    with pytest.raises(UnsignedCertificateError, match="unsigned"):
        issue(require_signature=True)


def test_require_signature_with_explicit_key(no_key_on_disk):
    key = Ed25519PrivateKey.generate()
    cert = issue(signing_key=key, require_signature=True)
    assert cert.signed is True
    assert cert.verify_signature(key.public_key())


def test_require_signature_with_key_on_disk(no_key_on_disk):
    generate_keypair(no_key_on_disk)
    cert = issue(require_signature=True)
    assert cert.signed is True


def test_signed_is_not_part_of_the_serialized_certificate(no_key_on_disk):
    cert = issue(signing_key=Ed25519PrivateKey.generate())
    assert "signed" not in cert.to_dict()
    assert VerificationCertificate.from_json(cert.to_json()).signed is True


def test_verification_refuses_unsigned_unless_told_otherwise(no_key_on_disk, tmp_path):
    crl = tmp_path / "crl.json"
    cert = issue()
    refused = verify_certificate(cert, crl_path=crl)
    assert not refused.valid and refused.status == "unsigned"
    assert verify_certificate(cert, crl_path=crl, require_signature=False).valid
