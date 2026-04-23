"""Export memory artifacts from trained agents."""

from ..api import call_api
from ..config import MODEL, MAX_TOKENS_EXPORT
from ..domains.base import Domain
from .schema import (
    MemoryArtifact,
    ArtifactDomain,
    ArtifactKnowledge,
    ArtifactProvenance,
    ArtifactAttestation,
)


def export_artifact(
    client,
    domain: Domain,
    accumulated_memory: list[str],
    agent_id: str = "",
    model: str = MODEL,
    sanitized: bool = False,
) -> MemoryArtifact:
    """Export a memory artifact from a trained agent.

    Sends the accumulated memory to the model and asks it to produce
    a structured, transferable knowledge export.

    Args:
        client: Anthropic API client
        domain: The domain configuration
        accumulated_memory: List of memory strings accumulated during training
        agent_id: Optional agent identifier
        model: Model to use

    Returns:
        A complete MemoryArtifact with schema, provenance, and hash.
    """
    if sanitized:
        export_prompt = domain.get_sanitized_export_prompt(accumulated_memory)
    else:
        export_prompt = domain.get_export_prompt(accumulated_memory)

    content = call_api(
        client=client,
        system=(
            "You are an expert agent exporting your learned knowledge as a "
            "structured memory artifact. Be specific, quantitative, and actionable. "
            "Another agent will use this to perform at your level without any "
            "of your direct experience."
        ),
        user_message=export_prompt,
        max_tokens=MAX_TOKENS_EXPORT,
        model=model,
    )

    # Detect sections in the exported content
    sections = []
    section_markers = [
        "calibration", "red_flags", "red flags", "mitigants",
        "heuristics", "mistakes", "scoring_guide", "scoring guide",
    ]
    content_lower = content.lower()
    for marker in section_markers:
        if marker in content_lower:
            sections.append(marker.replace(" ", "_"))

    # Build the formal artifact
    import uuid

    artifact = MemoryArtifact(
        domain=ArtifactDomain(
            category=domain.category,
            subcategory=domain.subcategory,
        ),
        knowledge=ArtifactKnowledge(
            format="markdown",
            content=content,
            sections=sections,
            token_count=len(content.split()),  # rough approximation
        ),
        provenance=ArtifactProvenance(
            agent_id=agent_id or str(uuid.uuid4()),
            model=model,
            training_rounds=domain.training_rounds,
            training_items=[item.name for item in domain.get_training_items()],
        ),
        attestation=ArtifactAttestation(),  # Filled in after evaluation
    )

    return artifact


def wrap_existing_artifact(
    content: str,
    domain: Domain,
    model: str = MODEL,
    agent_id: str = "",
    attestation: dict | None = None,
    training_rounds: int | None = None,
) -> MemoryArtifact:
    """Wrap an existing markdown artifact in the formal schema.

    Useful for wrapping artifacts from the original experiment.
    """
    import uuid

    sections = []
    section_markers = [
        "calibration", "red_flags", "red flags", "mitigants",
        "heuristics", "mistakes", "scoring_guide", "scoring guide",
    ]
    content_lower = content.lower()
    for marker in section_markers:
        if marker in content_lower:
            sections.append(marker.replace(" ", "_"))

    att = ArtifactAttestation(**(attestation or {}))

    return MemoryArtifact(
        domain=ArtifactDomain(
            category=domain.category,
            subcategory=domain.subcategory,
        ),
        knowledge=ArtifactKnowledge(
            format="markdown",
            content=content,
            sections=sections,
            token_count=len(content.split()),
        ),
        provenance=ArtifactProvenance(
            agent_id=agent_id or str(uuid.uuid4()),
            model=model,
            training_rounds=training_rounds or domain.training_rounds,
            training_items=[item.name for item in domain.get_training_items()],
        ),
        attestation=att,
    )
