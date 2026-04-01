"""Disposable sandbox agents for evaluation.

Key principle: each evaluation spawns a fresh agent with no memory.
The agent is injected with an optional artifact, runs the benchmark,
and is discarded. The buyer never touches the artifact during evaluation.
"""

from dataclasses import dataclass

from ..api import call_api_json
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

    metrics = {
        "novice_avg_error": novice_avg,
        "buyer_avg_error": buyer_avg,
        "improvement": novice_avg - buyer_avg,
        "transfer_efficiency_pct": (
            (novice_avg - buyer_avg) / novice_avg * 100 if novice_avg > 0 else 0
        ),
    }

    if expert_results:
        expert_avg = sum(r.error for r in expert_results) / len(expert_results)
        metrics["expert_avg_error"] = expert_avg
        gap = novice_avg - expert_avg
        metrics["relative_transfer_efficiency_pct"] = (
            (novice_avg - buyer_avg) / gap * 100 if gap > 0 else 0
        )

    return metrics
