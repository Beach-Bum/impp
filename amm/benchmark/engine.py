"""Domain-agnostic benchmark engine.

Orchestrates training, evaluation, and comparison across any domain.
"""

import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

from ..config import MODEL
from ..domains.base import Domain
from .training import train_expert
from .sandbox import evaluate_agent, compute_transfer_efficiency, AssessmentResult
from ..artifact.export import export_artifact
from ..artifact.schema import MemoryArtifact


@dataclass
class BenchmarkRun:
    """Results of a complete benchmark run."""

    id: str
    domain: str
    expert_results: list[AssessmentResult]
    novice_results: list[AssessmentResult]
    buyer_results: list[AssessmentResult]
    artifact: MemoryArtifact
    metrics: dict
    timestamp: str


def run_benchmark(
    client,
    domain: Domain,
    model: str = MODEL,
) -> BenchmarkRun:
    """Run a complete benchmark: train expert, evaluate all three agents.

    This is the full pipeline:
    1. Train expert over 20 rounds
    2. Export memory artifact
    3. Evaluate expert (with accumulated memory)
    4. Evaluate novice (no memory)
    5. Evaluate buyer (with exported artifact)
    6. Compute transfer metrics

    Returns a BenchmarkRun with all results.
    """
    run_id = str(uuid.uuid4())
    all_items = domain.get_all_items()

    # Step 1: Train expert
    accumulated_memory = train_expert(client, domain, model)

    # Step 2: Export artifact
    artifact = export_artifact(
        client=client,
        domain=domain,
        accumulated_memory=accumulated_memory,
        model=model,
    )

    # Step 3: Evaluate expert (with full training memory)
    expert_memory = "\n".join(accumulated_memory)
    expert_results = evaluate_agent(
        client, domain, items=all_items, memory=expert_memory, model=model
    )

    # Step 4: Evaluate novice (no memory)
    novice_results = evaluate_agent(
        client, domain, items=all_items, memory="", model=model
    )

    # Step 5: Evaluate buyer (with artifact only, using buyer-specific framing)
    buyer_prompt = domain.get_buyer_system_prompt(artifact.knowledge.content)
    buyer_results = evaluate_agent(
        client, domain, items=all_items, model=model,
        system_prompt_override=buyer_prompt,
    )

    # Step 6: Compute metrics
    metrics = compute_transfer_efficiency(
        novice_results=novice_results,
        buyer_results=buyer_results,
        expert_results=expert_results,
    )

    # Update artifact attestation
    artifact.attestation.expert_avg_error = metrics["expert_avg_error"]
    artifact.attestation.transfer_efficiency_pct = metrics.get(
        "relative_transfer_efficiency_pct", metrics["transfer_efficiency_pct"]
    )
    artifact.attestation.eval_items_count = len(all_items)
    artifact.attestation.trials = 1

    return BenchmarkRun(
        id=run_id,
        domain=domain.name,
        expert_results=expert_results,
        novice_results=novice_results,
        buyer_results=buyer_results,
        artifact=artifact,
        metrics=metrics,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


def run_verification_benchmark(
    client,
    domain: Domain,
    artifact_content: str,
    model: str = MODEL,
    novice_cache: list[AssessmentResult] | None = None,
) -> dict:
    """Run a verification-only benchmark (no training).

    Used by the referee protocol to verify an existing artifact.
    Evaluates a buyer agent (with artifact) vs novice baseline.

    Args:
        client: Anthropic API client
        domain: Domain configuration
        artifact_content: The artifact knowledge content to inject
        model: Model to use
        novice_cache: Optional cached novice results (saves API calls)

    Returns:
        Dict with buyer_results, novice_results, and metrics.
    """
    all_items = domain.get_all_items()

    # Novice baseline (use cache if available)
    if novice_cache:
        novice_results = novice_cache
    else:
        novice_results = evaluate_agent(
            client, domain, items=all_items, memory="", model=model
        )

    # Buyer with artifact (using buyer-specific framing)
    buyer_prompt = domain.get_buyer_system_prompt(artifact_content)
    buyer_results = evaluate_agent(
        client, domain, items=all_items, model=model,
        system_prompt_override=buyer_prompt,
    )

    metrics = compute_transfer_efficiency(
        novice_results=novice_results,
        buyer_results=buyer_results,
    )

    return {
        "buyer_results": buyer_results,
        "novice_results": novice_results,
        "metrics": metrics,
    }
