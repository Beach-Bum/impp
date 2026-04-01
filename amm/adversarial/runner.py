"""Adversarial probe runner — orchestrates all probes and computes aggregate score."""

from ..config import ADVERSARIAL_WEIGHTS, ADVERSARIAL_PASS_THRESHOLD, ADVERSARIAL_WARN_THRESHOLD
from ..domains.base import Domain
from ..benchmark.sandbox import AssessmentResult
from .bias_probe import run_bias_probe
from .consistency_probe import run_consistency_probe
from .stego_probe import run_stego_probe
from .overfit_probe import run_overfit_probe


def run_all_probes(
    client,
    domain: Domain,
    artifact_content: str,
    buyer_results: list[AssessmentResult],
    training_items: list[str],
    model: str = "",
) -> dict:
    """Run all adversarial probes and compute aggregate score.

    Args:
        client: Anthropic API client
        domain: Domain configuration
        artifact_content: The artifact knowledge content
        buyer_results: Results from referee/buyer evaluation (for overfit probe)
        training_items: Protocol names the artifact was trained on
        model: Model override

    Returns:
        {
            "aggregate_score": 0-100,
            "bias_score": float,
            "consistency_score": float,
            "stego_score": float,
            "overfit_score": float,
            "verdict": "PASS" | "WARN" | "FAIL",
            "all_flags": [str],
            "probe_details": {probe_name: full_result_dict},
        }
    """
    # Run each probe
    bias_result = run_bias_probe(client, domain, artifact_content, model)
    consistency_result = run_consistency_probe(client, domain, artifact_content, model)
    stego_result = run_stego_probe(client, artifact_content, model)
    overfit_result = run_overfit_probe(buyer_results, training_items)

    # Extract scores
    bias_score = bias_result["score"]
    consistency_score = consistency_result["score"]
    stego_score = stego_result["score"]
    overfit_score = overfit_result["score"]

    # Weighted aggregate
    aggregate = (
        ADVERSARIAL_WEIGHTS["bias"] * bias_score
        + ADVERSARIAL_WEIGHTS["consistency"] * consistency_score
        + ADVERSARIAL_WEIGHTS["stego"] * stego_score
        + ADVERSARIAL_WEIGHTS["overfit"] * overfit_score
    )

    # Collect all flags
    all_flags = (
        bias_result.get("flags", [])
        + consistency_result.get("flags", [])
        + stego_result.get("flags", [])
        + overfit_result.get("flags", [])
    )

    # Verdict
    if aggregate < ADVERSARIAL_PASS_THRESHOLD:
        verdict = "PASS"
    elif aggregate < ADVERSARIAL_WARN_THRESHOLD:
        verdict = "WARN"
    else:
        verdict = "FAIL"

    return {
        "aggregate_score": round(aggregate, 1),
        "bias_score": round(bias_score, 1),
        "consistency_score": round(consistency_score, 1),
        "stego_score": round(stego_score, 1),
        "overfit_score": round(overfit_score, 1),
        "verdict": verdict,
        "all_flags": all_flags,
        "probe_details": {
            "bias": bias_result,
            "consistency": consistency_result,
            "stego": stego_result,
            "overfit": overfit_result,
        },
    }
