"""Disposable sandbox agents for evaluation.

Key principle: each evaluation spawns a fresh agent with no memory.
The agent is injected with an optional artifact, runs the benchmark,
and is discarded. The buyer never touches the artifact during evaluation.
"""

import random
from dataclasses import dataclass

from ..api import call_api_json
from ..api_base import LLMClient
from ..config import MODEL, MAX_TOKENS_ASSESSMENT
from ..domains.base import Domain, EvalItem


@dataclass
class AssessmentResult:
    """Result of a single protocol assessment."""

    protocol: str
    agent_score: int
    true_score: int
    error: int
    reasoning: str
    confidence: str
    red_flags: list[str]


def evaluate_agent(
    client,
    domain: Domain,
    items: list[EvalItem] | None = None,
    memory: str = "",
    model: str = MODEL,
    system_prompt_override: str = "",
) -> list[AssessmentResult]:
    """Evaluate an agent on a set of items.

    This is a disposable evaluation — the agent starts fresh each time.
    If memory/artifact content is provided, it's injected into the system prompt.

    Args:
        client: Anthropic API client
        domain: Domain configuration
        items: Items to evaluate (defaults to all items)
        memory: Optional memory/artifact content to inject
        model: Model to use
        system_prompt_override: Optional full system prompt (bypasses memory injection)

    Returns:
        List of AssessmentResult for each item.
    """
    if items is None:
        items = domain.get_all_items()

    results = []
    system_prompt = system_prompt_override or domain.get_assessment_system_prompt(memory=memory)

    for item in items:
        result = call_api_json(
            client=client,
            system=system_prompt,
            user_message=domain.get_assessment_user_prompt(item),
            max_tokens=MAX_TOKENS_ASSESSMENT,
            model=model,
            default_on_failure={
                "score": 50,
                "reasoning": "Failed to parse response",
                "red_flags": [],
                "confidence": "low",
            },
        )

        score = result.get("score", 50)
        results.append(
            AssessmentResult(
                protocol=item.name,
                agent_score=score,
                true_score=item.true_score,
                error=abs(score - item.true_score),
                reasoning=result.get("reasoning", ""),
                confidence=result.get("confidence", "low"),
                red_flags=result.get("red_flags", []),
            )
        )

    return results


def evaluate_agent_llm(
    llm_client: LLMClient,
    domain: Domain,
    items: list[EvalItem] | None = None,
    system_prompt_override: str = "",
) -> list[AssessmentResult]:
    """Evaluate an agent using an LLMClient (for cross-model experiments).

    Same as evaluate_agent but uses the model-agnostic LLMClient protocol.
    """
    if items is None:
        items = domain.get_all_items()

    results = []
    system_prompt = system_prompt_override or domain.get_assessment_system_prompt()

    for item in items:
        result = llm_client.call_json(
            system=system_prompt,
            user_message=domain.get_assessment_user_prompt(item),
            max_tokens=MAX_TOKENS_ASSESSMENT,
            default_on_failure={
                "score": 50,
                "reasoning": "Failed to parse response",
                "red_flags": [],
                "confidence": "low",
            },
        )

        score = result.get("score", 50)
        results.append(
            AssessmentResult(
                protocol=item.name,
                agent_score=score,
                true_score=item.true_score,
                error=abs(score - item.true_score),
                reasoning=result.get("reasoning", ""),
                confidence=result.get("confidence", "low"),
                red_flags=result.get("red_flags", []),
            )
        )

    return results


def bootstrap_ci(
    novice_errors: list[float],
    buyer_errors: list[float],
    n_bootstrap: int = 1000,
    ci: float = 95.0,
) -> tuple[float, float]:
    """Compute bootstrap confidence interval for transfer efficiency.

    Resamples novice and buyer error arrays with replacement,
    computes TE for each sample, returns percentile bounds.

    Args:
        novice_errors: Per-item novice errors
        buyer_errors: Per-item buyer errors
        n_bootstrap: Number of bootstrap samples
        ci: Confidence level (default 95%)

    Returns:
        (lower_bound, upper_bound) as percentages
    """
    n = len(novice_errors)
    te_samples = []

    for _ in range(n_bootstrap):
        indices = [random.randint(0, n - 1) for _ in range(n)]
        nov_sample = [novice_errors[i] for i in indices]
        buy_sample = [buyer_errors[i] for i in indices]
        nov_avg = sum(nov_sample) / n
        buy_avg = sum(buy_sample) / n
        if nov_avg > 0:
            te_samples.append((nov_avg - buy_avg) / nov_avg * 100)

    if not te_samples:
        return (0.0, 0.0)

    te_samples.sort()
    alpha = (100 - ci) / 2
    lower_idx = max(0, int(len(te_samples) * alpha / 100))
    upper_idx = min(len(te_samples) - 1, int(len(te_samples) * (100 - alpha) / 100))

    return (round(te_samples[lower_idx], 1), round(te_samples[upper_idx], 1))


def paired_uplift_test(
    novice_results: list[AssessmentResult],
    buyer_results: list[AssessmentResult],
) -> dict:
    """Compute paired item-level uplift and Wilcoxon signed-rank test.

    For each item i: d_i = novice_error_i - buyer_error_i
    Positive d_i means the buyer improved over the novice.

    Returns:
        {
            "mean_uplift": mean of d_i,
            "median_uplift": median of d_i,
            "paired_diffs": list of d_i values,
            "items_improved": count where d_i > 0,
            "items_worsened": count where d_i < 0,
            "items_unchanged": count where d_i == 0,
            "wilcoxon_p": p-value from Wilcoxon signed-rank test (None if not computable),
            "significant_at_05": bool,
        }
    """
    # Match by protocol name
    novice_by_name = {r.protocol: r for r in novice_results}
    buyer_by_name = {r.protocol: r for r in buyer_results}

    diffs = []
    for name in novice_by_name:
        if name in buyer_by_name:
            d = novice_by_name[name].error - buyer_by_name[name].error
            diffs.append(d)

    if not diffs:
        return {"mean_uplift": 0, "paired_diffs": [], "wilcoxon_p": None, "significant_at_05": False}

    diffs_sorted = sorted(diffs)
    n = len(diffs)
    mean_d = sum(diffs) / n
    median_d = diffs_sorted[n // 2] if n % 2 else (diffs_sorted[n // 2 - 1] + diffs_sorted[n // 2]) / 2

    improved = sum(1 for d in diffs if d > 0)
    worsened = sum(1 for d in diffs if d < 0)
    unchanged = sum(1 for d in diffs if d == 0)

    # Wilcoxon signed-rank test (manual implementation to avoid scipy dependency)
    p_value = _wilcoxon_signed_rank(diffs)

    return {
        "mean_uplift": round(mean_d, 3),
        "median_uplift": round(median_d, 3),
        "paired_diffs": diffs,
        "items_improved": improved,
        "items_worsened": worsened,
        "items_unchanged": unchanged,
        "wilcoxon_p": round(p_value, 4) if p_value is not None else None,
        "significant_at_05": p_value is not None and p_value < 0.05,
    }


def _wilcoxon_signed_rank(diffs: list[float]) -> float | None:
    """Approximate Wilcoxon signed-rank test (two-sided).

    Uses normal approximation for n >= 10. Returns None if too few non-zero diffs.
    """
    import math

    # Remove zeros
    nonzero = [(abs(d), 1 if d > 0 else -1) for d in diffs if d != 0]
    n = len(nonzero)
    if n < 5:
        return None

    # Rank by absolute value
    nonzero.sort(key=lambda x: x[0])
    ranks = []
    i = 0
    while i < n:
        j = i + 1
        while j < n and nonzero[j][0] == nonzero[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2
        for k in range(i, j):
            ranks.append((avg_rank, nonzero[k][1]))
        i = j

    # W+ = sum of ranks for positive diffs
    w_plus = sum(r for r, sign in ranks if sign > 0)
    w_minus = sum(r for r, sign in ranks if sign < 0)
    w = min(w_plus, w_minus)

    # Normal approximation
    mean_w = n * (n + 1) / 4
    std_w = math.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    if std_w == 0:
        return None

    z = (w - mean_w) / std_w
    # Two-sided p-value from z using approximation
    p = 2 * (1 - _norm_cdf(abs(z)))
    return p


def _norm_cdf(z: float) -> float:
    """Approximate standard normal CDF (Abramowitz & Stegun)."""
    import math
    if z < 0:
        return 1 - _norm_cdf(-z)
    t = 1 / (1 + 0.2316419 * z)
    d = 0.3989422804014327  # 1/sqrt(2*pi)
    p = d * math.exp(-z * z / 2) * (
        t * (0.319381530 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429))))
    )
    return 1 - p


def compute_transfer_efficiency(
    novice_results: list[AssessmentResult],
    buyer_results: list[AssessmentResult],
    expert_results: list[AssessmentResult] | None = None,
    training_items: list[str] | None = None,
) -> dict:
    """Compute transfer efficiency and related metrics.

    Transfer Efficiency = (novice_error - buyer_error) / novice_error × 100

    If expert_results are provided, also computes relative to expert:
    Relative TE = (novice_error - buyer_error) / (novice_error - expert_error) × 100

    If training_items is provided, reports held-out-only metrics separately
    (the methodologically clean headline metric).
    """
    novice_avg = sum(r.error for r in novice_results) / len(novice_results)
    buyer_avg = sum(r.error for r in buyer_results) / len(buyer_results)

    novice_errors = [r.error for r in novice_results]
    buyer_errors = [r.error for r in buyer_results]
    ci_lower, ci_upper = bootstrap_ci(novice_errors, buyer_errors)

    # Paired uplift test
    paired = paired_uplift_test(novice_results, buyer_results)

    metrics = {
        "novice_avg_error": novice_avg,
        "buyer_avg_error": buyer_avg,
        "improvement": novice_avg - buyer_avg,
        "transfer_efficiency_pct": (
            (novice_avg - buyer_avg) / novice_avg * 100 if novice_avg > 0 else 0
        ),
        "confidence_interval_95": [ci_lower, ci_upper],
        "paired_uplift": paired,
    }

    if expert_results:
        expert_avg = sum(r.error for r in expert_results) / len(expert_results)
        metrics["expert_avg_error"] = expert_avg
        gap = novice_avg - expert_avg
        metrics["relative_transfer_efficiency_pct"] = (
            (novice_avg - buyer_avg) / gap * 100 if gap > 0 else 0
        )

    # Held-out-only metrics (the clean headline number)
    if training_items:
        training_set = set(training_items)
        novice_ho = [r for r in novice_results if r.protocol not in training_set]
        buyer_ho = [r for r in buyer_results if r.protocol not in training_set]
        novice_seen = [r for r in novice_results if r.protocol in training_set]
        buyer_seen = [r for r in buyer_results if r.protocol in training_set]

        if novice_ho and buyer_ho:
            nov_ho_avg = sum(r.error for r in novice_ho) / len(novice_ho)
            buy_ho_avg = sum(r.error for r in buyer_ho) / len(buyer_ho)
            ho_te = (nov_ho_avg - buy_ho_avg) / nov_ho_avg * 100 if nov_ho_avg > 0 else 0
            ho_paired = paired_uplift_test(novice_ho, buyer_ho)

            metrics["held_out"] = {
                "count": len(novice_ho),
                "novice_avg_error": round(nov_ho_avg, 2),
                "buyer_avg_error": round(buy_ho_avg, 2),
                "transfer_efficiency_pct": round(ho_te, 1),
                "paired_uplift": ho_paired,
            }

        if novice_seen and buyer_seen:
            nov_seen_avg = sum(r.error for r in novice_seen) / len(novice_seen)
            buy_seen_avg = sum(r.error for r in buyer_seen) / len(buyer_seen)
            seen_te = (nov_seen_avg - buy_seen_avg) / nov_seen_avg * 100 if nov_seen_avg > 0 else 0

            metrics["training_items"] = {
                "count": len(novice_seen),
                "novice_avg_error": round(nov_seen_avg, 2),
                "buyer_avg_error": round(buy_seen_avg, 2),
                "transfer_efficiency_pct": round(seen_te, 1),
            }

    return metrics
