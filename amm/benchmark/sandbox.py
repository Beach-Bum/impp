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


def compute_transfer_efficiency(
    novice_results: list[AssessmentResult],
    buyer_results: list[AssessmentResult],
    expert_results: list[AssessmentResult] | None = None,
) -> dict:
    """Compute transfer efficiency and related metrics.

    Transfer Efficiency = (novice_error - buyer_error) / novice_error × 100

    If expert_results are provided, also computes relative to expert:
    Relative TE = (novice_error - buyer_error) / (novice_error - expert_error) × 100
    """
    novice_avg = sum(r.error for r in novice_results) / len(novice_results)
    buyer_avg = sum(r.error for r in buyer_results) / len(buyer_results)

    novice_errors = [r.error for r in novice_results]
    buyer_errors = [r.error for r in buyer_results]
    ci_lower, ci_upper = bootstrap_ci(novice_errors, buyer_errors)

    metrics = {
        "novice_avg_error": novice_avg,
        "buyer_avg_error": buyer_avg,
        "improvement": novice_avg - buyer_avg,
        "transfer_efficiency_pct": (
            (novice_avg - buyer_avg) / novice_avg * 100 if novice_avg > 0 else 0
        ),
        "confidence_interval_95": [ci_lower, ci_upper],
    }

    if expert_results:
        expert_avg = sum(r.error for r in expert_results) / len(expert_results)
        metrics["expert_avg_error"] = expert_avg
        gap = novice_avg - expert_avg
        metrics["relative_transfer_efficiency_pct"] = (
            (novice_avg - buyer_avg) / gap * 100 if gap > 0 else 0
        )

    return metrics
