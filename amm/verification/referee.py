"""Referee Protocol — the core verification orchestrator.

Implements the 8-step verification flow:
1. Submit artifact
2. Select benchmark
3. Spawn novice baseline
4. Spawn referee (disposable, with artifact)
5. Differential scoring
6. Adversarial probes
7. Generate certificate
8. Update trust score
"""

import hashlib
import json
import uuid
from datetime import datetime, timezone

from ..api import create_client
from ..config import MODEL, TRUST_WEIGHTS
from ..artifact.schema import MemoryArtifact
from ..domains.base import Domain
from ..benchmark.engine import run_verification_benchmark
from ..benchmark.sandbox import AssessmentResult
from ..adversarial.runner import run_all_probes
from .certificate import generate_certificate, VerificationCertificate


def compute_trust_score(
    transfer_efficiency: float,
    adversarial_score: float,
    freshness_pct: float = 100.0,
) -> float:
    """Compute composite trust score.

    trust = 0.50 × transfer_efficiency + 0.30 × (100 - adversarial) + 0.20 × freshness

    Transfer efficiency is clamped to [-100, 100] — negative TE actively
    penalizes the trust score rather than being clipped to 0.
    Adversarial and freshness are clamped to [0, 100].
    """
    # Allow negative TE to penalize trust score (not clipped to 0)
    te_clamped = min(100, max(-100, transfer_efficiency))
    return (
        TRUST_WEIGHTS["transfer_efficiency"] * te_clamped
        + TRUST_WEIGHTS["adversarial_clean"] * (100 - min(100, max(0, adversarial_score)))
        + TRUST_WEIGHTS["freshness"] * min(100, max(0, freshness_pct))
    )


def verify_artifact(
    artifact: MemoryArtifact,
    domain: Domain,
    client=None,
    model: str = MODEL,
    novice_cache: list[AssessmentResult] | None = None,
) -> VerificationCertificate:
    """Run the full verification protocol on a memory artifact.

    This is the main entry point for artifact verification.

    Args:
        artifact: The memory artifact to verify
        domain: Domain configuration
        client: Optional Anthropic client (creates one if not provided)
        model: Model to use
        novice_cache: Optional cached novice results

    Returns:
        A VerificationCertificate with all results.
    """
    if client is None:
        client = create_client()

    # Step 1: Validate artifact
    issues = artifact.validate()
    if issues:
        raise ValueError(f"Artifact validation failed: {issues}")

    # Step 2: Benchmark info
    benchmark_id = str(uuid.uuid4())
    all_items = domain.get_all_items()
    held_out = domain.get_held_out_items()

    benchmark_config = json.dumps(
        {"domain": domain.name, "items": [i.name for i in all_items]},
        sort_keys=True,
    )
    benchmark_hash = hashlib.sha256(benchmark_config.encode()).hexdigest()

    benchmark_info = {
        "id": benchmark_id,
        "domain": domain.name,
        "protocol_count": len(all_items),
        "held_out_count": len(held_out),
        "hash": benchmark_hash,
    }

    # Steps 3-5: Run verification benchmark (novice + buyer + differential)
    bench_results = run_verification_benchmark(
        client=client,
        domain=domain,
        artifact_content=artifact.knowledge.content,
        model=model,
        novice_cache=novice_cache,
    )

    metrics = bench_results["metrics"]
    buyer_results = bench_results["buyer_results"]
    te = metrics.get("transfer_efficiency_pct", 0)

    # Step 6: Adversarial probes
    training_items = artifact.provenance.training_items
    adversarial = run_all_probes(
        client=client,
        domain=domain,
        artifact_content=artifact.knowledge.content,
        buyer_results=buyer_results,
        training_items=training_items,
        model=model,
        transfer_efficiency=te,
    )

    # Step 7: Compute trust score and generate certificate
    trust = compute_trust_score(
        transfer_efficiency=te,
        adversarial_score=adversarial["aggregate_score"],
    )

    # Build results dict for certificate
    results_dict = {
        "buyer_avg_error": metrics["buyer_avg_error"],
        "novice_avg_error": metrics["novice_avg_error"],
        "transfer_efficiency_pct": round(te, 1),
        "per_protocol": {
            r.protocol: {
                "agent_score": r.agent_score,
                "true_score": r.true_score,
                "error": r.error,
            }
            for r in buyer_results
        },
    }

    certificate = generate_certificate(
        artifact_hash=artifact.hash,
        benchmark_info=benchmark_info,
        results=results_dict,
        adversarial=adversarial,
        trust_score=trust,
        referee_model=model,
    )

    return certificate
