"""Overfitting Probe — detect memorization vs generalization.

Compares artifact-enhanced agent performance on:
- Seen protocols (in the artifact's training set)
- Unseen protocols (held out during training)

A well-generalized artifact should perform similarly on both.
An overfitted artifact will excel on seen protocols but struggle on unseen ones.

Weight: 0.20 of aggregate adversarial score.
"""

from ..benchmark.sandbox import AssessmentResult


def run_overfit_probe(
    buyer_results: list[AssessmentResult],
    training_items: list[str],
) -> dict:
    """Run overfitting detection using existing evaluation data.

    This probe does NOT require additional API calls — it analyzes
    the results from the referee evaluation.

    Args:
        buyer_results: Results from the artifact-enhanced evaluation
        training_items: List of protocol names the artifact was trained on

    Returns:
        {
            "score": 0-100 (higher = more overfitted),
            "seen_avg_error": float,
            "unseen_avg_error": float,
            "overfit_ratio": float,
            "flags": [str],
        }
    """
    training_set = set(training_items)

    seen_errors = [r.error for r in buyer_results if r.protocol in training_set]
    unseen_errors = [r.error for r in buyer_results if r.protocol not in training_set]

    if not seen_errors or not unseen_errors:
        return {
            "score": 0,
            "seen_avg_error": 0,
            "unseen_avg_error": 0,
            "overfit_ratio": 1.0,
            "flags": ["INCOMPLETE: insufficient data for seen/unseen split"],
        }

    seen_avg = sum(seen_errors) / len(seen_errors)
    unseen_avg = sum(unseen_errors) / len(unseen_errors)

    # Overfit ratio: how much better on seen vs unseen
    # 1.0 = perfect generalization, <0.3 = severe overfitting
    overfit_ratio = seen_avg / max(unseen_avg, 0.1)

    # Score: 0 (no overfitting) to 100 (severe overfitting)
    # Ratio of 1.0 → score 0
    # Ratio of 0.5 → score 50
    # Ratio of 0.0 → score 100
    if overfit_ratio >= 1.0:
        # Seen errors >= unseen errors (no overfitting, possibly underfitting)
        score = 0
    else:
        score = (1.0 - overfit_ratio) * 100

    flags = []
    if score > 50:
        flags.append(
            f"OVERFIT:severe — seen_error={seen_avg:.1f}, unseen_error={unseen_avg:.1f}, "
            f"ratio={overfit_ratio:.2f}. Artifact may have memorized training data."
        )
    elif score > 25:
        flags.append(
            f"OVERFIT:moderate — seen_error={seen_avg:.1f}, unseen_error={unseen_avg:.1f}, "
            f"ratio={overfit_ratio:.2f}. Some overfitting detected."
        )

    return {
        "score": round(min(100, score), 1),
        "seen_avg_error": round(seen_avg, 2),
        "unseen_avg_error": round(unseen_avg, 2),
        "overfit_ratio": round(overfit_ratio, 3),
        "flags": flags,
    }
