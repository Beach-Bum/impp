"""Memory Artifact schema: M = (D, K, P, A, H).

Formal definition from the working paper (Section 2.1):
  D (Domain) — structured identifier for the knowledge domain
  K (Knowledge) — the learned content (heuristics, calibration data, patterns)
  P (Provenance) — metadata about the artifact's origin
  A (Attestation) — verifiable performance claims
  H (Hash) — content-addressed identifier for integrity verification
"""

import hashlib
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone


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


@dataclass
class ArtifactAttestation:
    """A — Performance claims."""

    expert_avg_error: float = 0.0
    transfer_efficiency_pct: float = 0.0
    eval_items_count: int = 0
    trials: int = 0


@dataclass
class MemoryArtifact:
    """Complete memory artifact M = (D, K, P, A, H)."""

    domain: ArtifactDomain
    knowledge: ArtifactKnowledge
    provenance: ArtifactProvenance
    attestation: ArtifactAttestation
    version: str = "0.1.0"
    hash: str = ""

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

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        d = asdict(self)
        return d

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: dict) -> "MemoryArtifact":
        """Deserialize from dictionary."""
        artifact = cls(
            version=data.get("version", "0.1.0"),
            domain=ArtifactDomain(**data["domain"]),
            knowledge=ArtifactKnowledge(**data["knowledge"]),
            provenance=ArtifactProvenance(**data["provenance"]),
            attestation=ArtifactAttestation(**data["attestation"]),
            hash=data.get("hash", ""),
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

        # Verify hash integrity
        computed = self.compute_hash()
        if self.hash and self.hash != computed:
            issues.append(f"Hash integrity check failed")

        return issues
