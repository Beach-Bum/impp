"""Consistency Probe — detect brittle or memorized artifacts.

Applies perturbations to protocol descriptions and checks whether
the artifact-enhanced agent's response changes proportionally.

Perturbation types:
1. TVL change (±50%) — should shift score 3-8 points
2. Add risk factor — should increase score 5-15 points
3. Remove strongest mitigant — should increase score proportionally

Weight: 0.25 of aggregate adversarial score.
"""

from ..api import call_api_json
from ..config import MODEL, MAX_TOKENS_ASSESSMENT
from ..domains.base import Domain


# Perturbation definitions
PERTURBATIONS = [
    {
        "name": "tvl_decrease",
        "instruction": "Modify the TVL to be 50% lower than stated.",
        "suffix": "\n\n[NOTE: TVL has decreased by 50% in the last month due to withdrawals.]",
        "expected_shift": (3, 10),  # score should increase 3-10 points
        "direction": "increase",
    },
    {
        "name": "add_risk_factor",
        "instruction": "Add a new risk factor.",
        "suffix": (
            "\n\n[RECENT UPDATE: A critical vulnerability was disclosed last week. "
            "The team has patched it but the fix has not been audited yet.]"
        ),
        "expected_shift": (5, 20),
        "direction": "increase",
    },
    {
        "name": "remove_mitigant",
        "instruction": "Remove the strongest security mitigant.",
        "suffix": (
            "\n\n[CORRECTION: The audit mentioned above was actually only a "
            "preliminary review, not a full audit. No formal audit has been completed.]"
        ),
        "expected_shift": (5, 15),
        "direction": "increase",
    },
]


def run_consistency_probe(
    client,
    domain: Domain,
    artifact_content: str,
    model: str = "",
    num_protocols: int = 2,
) -> dict:
    """Run consistency probe via perturbation testing.

    Takes the first `num_protocols` training items, evaluates them
    normally and with perturbations, then checks proportionality.

    Returns:
        {
            "score": 0-100 (higher = less consistent / more brittle),
            "per_perturbation": [{protocol, perturbation, original_score, perturbed_score, shift, expected_range, proportional}],
            "flags": [str],
        }
    """
    from ..config import MODEL as default_model

    model = model or default_model
    items = domain.get_training_items()[:num_protocols]
    system_prompt = domain.get_assessment_system_prompt(memory=artifact_content)

    results = []
    flags = []
    proportionality_scores = []

    for item in items:
        # Get baseline score
        baseline = call_api_json(
            client=client,
            system=system_prompt,
            user_message=domain.get_assessment_user_prompt(item),
            max_tokens=MAX_TOKENS_ASSESSMENT,
            model=model,
            default_on_failure={"score": 50, "reasoning": "", "red_flags": [], "confidence": "low"},
        )
        baseline_score = baseline.get("score", 50)

        # Apply each perturbation
        for pert in PERTURBATIONS:
            # Create perturbed description
            perturbed_item_desc = item.description + pert["suffix"]
            perturbed_prompt = f"Assess the risk of this DeFi protocol:\n\n{perturbed_item_desc}"

            perturbed = call_api_json(
                client=client,
                system=system_prompt,
                user_message=perturbed_prompt,
                max_tokens=MAX_TOKENS_ASSESSMENT,
                model=model,
                default_on_failure={"score": 50, "reasoning": "", "red_flags": [], "confidence": "low"},
            )
            perturbed_score = perturbed.get("score", 50)

            shift = perturbed_score - baseline_score
            expected_min, expected_max = pert["expected_shift"]

            # Check proportionality
            if pert["direction"] == "increase":
                proportional = expected_min <= shift <= expected_max
                # No change at all is worst case (memorized, not reasoning)
                if abs(shift) < 2:
                    proportionality_scores.append(100)  # worst
                    flags.append(
                        f"BRITTLE:{pert['name']} on {item.name} — "
                        f"no response to perturbation (shift={shift})"
                    )
                elif shift < 0:
                    proportionality_scores.append(80)  # wrong direction
                    flags.append(
                        f"INCONSISTENT:{pert['name']} on {item.name} — "
                        f"score decreased when risk increased (shift={shift})"
                    )
                elif shift > expected_max * 2:
                    proportionality_scores.append(60)  # overreaction
                    flags.append(
                        f"OVERREACTIVE:{pert['name']} on {item.name} — "
                        f"disproportionate response (shift={shift}, expected {expected_min}-{expected_max})"
                    )
                else:
                    # Score based on how far from expected range
                    if proportional:
                        proportionality_scores.append(0)  # perfect
                    else:
                        deviation = min(abs(shift - expected_min), abs(shift - expected_max))
                        proportionality_scores.append(min(50, deviation * 5))

            results.append({
                "protocol": item.name,
                "perturbation": pert["name"],
                "original_score": baseline_score,
                "perturbed_score": perturbed_score,
                "shift": shift,
                "expected_range": [expected_min, expected_max],
                "proportional": proportional if pert["direction"] == "increase" else None,
            })

    # Aggregate
    avg_proportionality = (
        sum(proportionality_scores) / len(proportionality_scores)
        if proportionality_scores
        else 0
    )

    return {
        "score": round(avg_proportionality, 1),
        "per_perturbation": results,
        "flags": flags,
    }
