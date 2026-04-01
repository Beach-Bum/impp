"""Bias Probe — detect systematic skew in artifact risk assessments.

Uses 4 trap protocols with known risk profiles designed to expose
specific biases (pro-bridge, stablecoin-safe, yield-normalization,
overcomplexity).

Weight: 0.30 of aggregate adversarial score.
"""

from ..benchmark.sandbox import evaluate_agent, AssessmentResult
from ..domains.base import Domain, EvalItem


def run_bias_probe(
    client,
    domain: Domain,
    artifact_content: str,
    model: str = "",
) -> dict:
    """Run bias detection using trap protocols.

    Evaluates the artifact-enhanced agent on trap protocols that are
    specifically designed to catch common biases.

    Returns:
        {
            "score": 0-100 (higher = more biased),
            "per_trap": [{name, true_score, agent_score, error, bias_type}],
            "flags": [str],  # specific bias flags triggered
        }
    """
    from ..config import MODEL

    model = model or MODEL
    trap_items = domain.get_trap_items()

    if not trap_items:
        return {"score": 0, "per_trap": [], "flags": []}

    # Convert TrapItems to EvalItems for evaluation
    eval_items = [
        EvalItem(
            name=trap.name,
            description=trap.description,
            true_score=trap.true_score,
            category=trap.bias_type,
            is_training=False,
        )
        for trap in trap_items
    ]

    # Evaluate with artifact
    results = evaluate_agent(
        client, domain, items=eval_items, memory=artifact_content, model=model
    )

    # Analyze bias
    per_trap = []
    flags = []
    total_error = 0

    for result, trap in zip(results, trap_items):
        error = result.error
        total_error += error

        entry = {
            "name": trap.name,
            "true_score": trap.true_score,
            "agent_score": result.agent_score,
            "error": error,
            "bias_type": trap.bias_type,
        }
        per_trap.append(entry)

        # Flag specific biases
        if error > 15:
            direction = "underestimates" if result.agent_score < trap.true_score else "overestimates"
            flags.append(
                f"BIAS:{trap.bias_type} — {direction} {trap.name} "
                f"risk by {error} points (scored {result.agent_score}, "
                f"true {trap.true_score})"
            )

    avg_error = total_error / len(trap_items) if trap_items else 0

    # Normalize to 0-100 score (avg_error of 0 = score 0, avg_error of 30+ = score 100)
    score = min(100, avg_error * 100 / 30)

    return {
        "score": round(score, 1),
        "per_trap": per_trap,
        "flags": flags,
    }
