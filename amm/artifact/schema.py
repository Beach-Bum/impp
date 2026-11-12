"""Memory Artifact schema: M = (D, K, P, A, H).

Formal definition from the working paper (Section 2.1):
  D (Domain) — structured identifier for the knowledge domain
  K (Knowledge) — the learned content (heuristics, calibration data, patterns)
  P (Provenance) — metadata about the artifact's origin
  A (Attestation) — verifiable performance claims
  H (Hash) — content-addressed identifier for integrity verification

Schema version: 0.2
"""

import hashlib
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone

VALID_ARTIFACT_TYPES = ("procedural", "semantic", "episodic_derived", "hybrid")
VALID_ATTACH_MODES = (
    "prepend_policy",
    "few_shot_examples",
    "retrieval_only",
    "tool_policy",
    "read_only_reference",
)
VALID_LICENSES = (
    "MIT",
    "Apache-2.0",
    "CC-BY-4.0",
    "CC-BY-SA-4.0",
    "CC-BY-NC-4.0",
    "proprietary",
)


INTEGRITY_PREFIX = "sha256:"
_INTEGRITY_DOMAIN = b"impp-artifact-integrity-v1:"


def integrity_digest(data: dict) -> str:
    """Full-coverage integrity digest of a serialized artifact.

    SHA-256 over the canonical JSON (sorted keys, no insignificant
    whitespace) of the whole artifact dictionary, minus the ``integrity``
    field itself. Unlike ``MemoryArtifact.compute_hash`` (the content
    address, which covers four fields), every key and every leaf value is
    covered: attestation, provenance, card, privacy, revocation, and any
    field added later.

    The digest is not a signature: whoever can rewrite the file can also
    recompute it. It becomes tamper-evident when it is bound into a signed
    verification certificate (``VerificationCertificate.artifact_integrity``).
    """
    body = {k: v for k, v in data.items() if k != "integrity"}
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("ascii")
    return INTEGRITY_PREFIX + hashlib.sha256(_INTEGRITY_DOMAIN + canonical).hexdigest()


# ── New v0.2 dataclasses ──────────────────────────────────────────────


@dataclass
class SourceMaterial:
    """Reference to source data."""

    name: str = ""
    url: str = ""
    license: str = ""


@dataclass
class EvaluationSuite:
    """Metadata about the evaluation benchmark."""

    name: str = ""
    version: str = ""
    held_out_count: int = 0
    benchmark_hash: str = ""


@dataclass
class AttachConfig:
    """Runtime attach mode configuration."""

    supported_modes: list[str] = field(
        default_factory=lambda: ["prepend_policy"]
    )
    default_mode: str = "prepend_policy"
    prohibited_modes: list[str] = field(default_factory=list)


@dataclass
class ArtifactCard:
    """Artifact card — intended use, contraindications, known failures."""

    intended_use: str = ""
    contraindications: list[str] = field(default_factory=list)
    known_failures: list[str] = field(default_factory=list)
    limitations: str = ""


@dataclass
class PrivacyMetadata:
    """Privacy flags."""

    contains_pii: bool = False
    pii_redacted: bool = False
    data_jurisdiction: str = ""


@dataclass
class ConflictDeclaration:
    """Declared conflict with another artifact."""

    artifact: str = ""
    reason: str = ""


@dataclass
class RevocationStatus:
    """Revocation state."""

    revoked: bool = False
    revoked_at: str = ""
    revocation_reason: str = ""


# ── Core M = (D, K, P, A, H) dataclasses ──────────────────────────────


@dataclass
class ArtifactDomain:
    """D — Domain identifier."""

    category: str  # e.g., "DeFi"
    subcategory: str  # e.g., "risk-assessment"
    scope: str = "protocol-level"


@dataclass
class ArtifactKnowledge:
    """K — The learned content."""

    format: str  # e.g., "markdown"
    content: str  # The actual artifact text
    sections: list[str] = field(default_factory=list)
    token_count: int = 0


@dataclass
class ArtifactProvenance:
    """P — Metadata about origin."""

    agent_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    model: str = ""
    training_rounds: int = 0
    training_items: list[str] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    experiment_version: str = "0.1.0"
    # v0.2 additions
    license: str = ""
    license_url: str = ""
    source_material: list[SourceMaterial] = field(default_factory=list)


@dataclass
class ArtifactAttestation:
    """A — Performance claims."""

    expert_avg_error: float = 0.0
    transfer_efficiency_pct: float = 0.0
    eval_items_count: int = 0
    trials: int = 0
    # v0.2 addition
    evaluation_suite: EvaluationSuite = field(default_factory=EvaluationSuite)


@dataclass
class MemoryArtifact:
    """Complete memory artifact M = (D, K, P, A, H)."""

    domain: ArtifactDomain
    knowledge: ArtifactKnowledge
    provenance: ArtifactProvenance
    attestation: ArtifactAttestation
    version: str = "0.1.0"
    hash: str = ""
    # v0.2 additions
    artifact_type: str = ""
    attach: AttachConfig = field(default_factory=AttachConfig)
    card: ArtifactCard = field(default_factory=ArtifactCard)
    privacy: PrivacyMetadata = field(default_factory=PrivacyMetadata)
    conflicts: list[ConflictDeclaration] = field(default_factory=list)
    revocation: RevocationStatus = field(default_factory=RevocationStatus)
    # Full-coverage integrity digest (see integrity_digest). Empty on
    # artifacts published before the digest existed, and until seal() is called.
    integrity: str = ""

    def __post_init__(self):
        if not self.hash:
            self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        """Compute SHA-256 content-addressed hash.

        Hash is deterministic from: domain + knowledge content + agent_id + created_at.
        This ensures the same artifact always produces the same hash.
        """
        canonical = (
            f"{self.domain.category}:{self.domain.subcategory}"
            f"|{self.knowledge.content}"
            f"|{self.provenance.agent_id}"
            f"|{self.provenance.created_at}"
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def compute_integrity(self) -> str:
        """Compute the full-coverage integrity digest of this artifact.

        Covers every field (including ``hash``) except ``integrity`` itself.
        The content address returned by compute_hash() is left unchanged.
        """
        return integrity_digest(self.to_dict())

    def seal(self) -> "MemoryArtifact":
        """Record the integrity digest. Call once the artifact is final
        (e.g. after the attestation has been filled in), before publishing."""
        self.integrity = self.compute_integrity()
        return self

    def integrity_status(self) -> str:
        """Return "verified", "mismatch", or "absent".

        "absent" means the artifact carries no integrity digest (it predates
        the digest, or was never sealed). That is reported, not treated as a
        failure: only the fields in compute_hash() are protected for it.
        """
        if not self.integrity:
            return "absent"
        return "verified" if self.integrity == self.compute_integrity() else "mismatch"

    def verify_integrity(self) -> bool:
        """True unless an integrity digest is present and does not match."""
        return self.integrity_status() != "mismatch"

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        d = asdict(self)
        # Unsealed artifacts serialize exactly as they did before the
        # integrity digest was introduced.
        if not d.get("integrity"):
            d.pop("integrity", None)
        return d

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: dict) -> "MemoryArtifact":
        """Deserialize from dictionary."""
        # Check the full-coverage digest against the data exactly as given,
        # before any field is defaulted or dropped by reconstruction.
        # Artifacts without a digest (older format) are still accepted.
        declared_integrity = data.get("integrity", "")
        if declared_integrity:
            computed_integrity = integrity_digest(data)
            if computed_integrity != declared_integrity:
                raise ValueError(
                    f"Integrity digest mismatch: expected {declared_integrity}, "
                    f"computed {computed_integrity}. "
                    "Artifact may have been tampered with."
                )

        # Nested dataclass reconstruction
        domain_data = data.get("domain", {})
        knowledge_data = data.get("knowledge", {})
        # Copied: the pops below must not alter the caller's dictionary
        provenance_data = dict(data.get("provenance", {}))
        attestation_data = dict(data.get("attestation", {}))

        # Handle source_material list in provenance
        source_raw = provenance_data.pop("source_material", [])
        source_material = [SourceMaterial(**s) for s in source_raw]

        # Handle evaluation_suite in attestation
        eval_suite_raw = attestation_data.pop("evaluation_suite", {})
        eval_suite = EvaluationSuite(**eval_suite_raw) if eval_suite_raw else EvaluationSuite()

        # Handle v0.2 top-level nested objects
        attach_raw = data.get("attach", {})
        card_raw = data.get("card", {})
        privacy_raw = data.get("privacy", {})
        conflicts_raw = data.get("conflicts", [])
        revocation_raw = data.get("revocation", {})

        artifact = cls(
            version=data.get("version", "0.1.0"),
            domain=ArtifactDomain(**domain_data),
            knowledge=ArtifactKnowledge(**knowledge_data),
            provenance=ArtifactProvenance(
                **provenance_data, source_material=source_material
            ),
            attestation=ArtifactAttestation(
                **attestation_data, evaluation_suite=eval_suite
            ),
            hash=data.get("hash", ""),
            artifact_type=data.get("artifact_type", ""),
            attach=AttachConfig(**attach_raw) if attach_raw else AttachConfig(),
            card=ArtifactCard(**card_raw) if card_raw else ArtifactCard(),
            privacy=PrivacyMetadata(**privacy_raw) if privacy_raw else PrivacyMetadata(),
            conflicts=[ConflictDeclaration(**c) for c in conflicts_raw],
            revocation=RevocationStatus(**revocation_raw) if revocation_raw else RevocationStatus(),
            integrity=declared_integrity,
        )
        # Recompute and verify hash if provided
        if data.get("hash"):
            computed = artifact.compute_hash()
            if computed != data["hash"]:
                raise ValueError(
                    f"Hash mismatch: expected {data['hash']}, computed {computed}. "
                    "Artifact may have been tampered with."
                )
        return artifact

    @classmethod
    def from_json(cls, json_str: str) -> "MemoryArtifact":
        """Deserialize from JSON string."""
        return cls.from_dict(json.loads(json_str))

    def validate(self) -> list[str]:
        """Validate the artifact. Returns list of issues (empty = valid)."""
        issues = []

        if not self.domain.category:
            issues.append("domain.category is required")
        if not self.domain.subcategory:
            issues.append("domain.subcategory is required")
        if not self.knowledge.content:
            issues.append("knowledge.content is empty")
        if self.knowledge.format not in ("markdown", "json", "text"):
            issues.append(f"Unknown knowledge format: {self.knowledge.format}")
        if not self.provenance.agent_id:
            issues.append("provenance.agent_id is required")
        if not self.provenance.model:
            issues.append("provenance.model is required")

        # v0.2 validations
        if self.artifact_type and self.artifact_type not in VALID_ARTIFACT_TYPES:
            issues.append(f"Unknown artifact_type: {self.artifact_type}")

        if self.provenance.license and self.provenance.license not in VALID_LICENSES:
            issues.append(f"Unknown license: {self.provenance.license}")

        for mode in self.attach.supported_modes:
            if mode not in VALID_ATTACH_MODES:
                issues.append(f"Unknown attach mode: {mode}")
        if self.attach.default_mode not in VALID_ATTACH_MODES:
            issues.append(f"Unknown default attach mode: {self.attach.default_mode}")
        if self.attach.default_mode not in self.attach.supported_modes:
            issues.append("default_mode must be in supported_modes")

        if self.privacy.contains_pii and not self.privacy.pii_redacted:
            issues.append("Artifact contains PII but pii_redacted is false")

        if self.revocation.revoked and not self.revocation.revoked_at:
            issues.append("Revoked artifact must have revoked_at timestamp")

        # Verify hash integrity
        computed = self.compute_hash()
        if self.hash and self.hash != computed:
            issues.append("Hash integrity check failed")

        # Verify the full-coverage digest when the artifact carries one
        if self.integrity_status() == "mismatch":
            issues.append("Integrity digest check failed")

        return issues
