"""Verification certificate generation and validation."""

import json
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta

from ..config import CERTIFICATE_EXPIRY_DAYS


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

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def is_expired(self) -> bool:
        expiry = datetime.fromisoformat(self.expires_at)
        return datetime.now(timezone.utc) > expiry

    @classmethod
    def from_dict(cls, data: dict) -> "VerificationCertificate":
        return cls(**data)


def generate_certificate(
    artifact_hash: str,
    benchmark_info: dict,
    results: dict,
    adversarial: dict,
    trust_score: float,
    referee_model: str,
    expiry_days: int = CERTIFICATE_EXPIRY_DAYS,
) -> VerificationCertificate:
    """Generate a verification certificate.

    Args:
        artifact_hash: Hash of the verified artifact
        benchmark_info: Benchmark metadata
        results: Evaluation results (metrics, per_protocol)
        adversarial: Adversarial probe results
        trust_score: Computed trust score
        referee_model: Model used for verification
        expiry_days: Days until certificate expires

    Returns:
        A VerificationCertificate.
    """
    now = datetime.now(timezone.utc)

    return VerificationCertificate(
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
    )
