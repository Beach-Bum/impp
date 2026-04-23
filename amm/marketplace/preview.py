"""Artifact preview generation.

Produces a preview that reveals metadata and structure
without exposing the knowledge content — the "window shopping" view.
"""

from ..artifact.schema import MemoryArtifact


def generate_preview(
    artifact: MemoryArtifact,
    trust_data: dict | None = None,
    latest_verification: dict | None = None,
) -> dict:
    """Generate a buyer preview for a memory artifact.

    Shows everything EXCEPT the actual knowledge content.

    Args:
        artifact: The full memory artifact
        trust_data: Trust score data from registry (optional)
        latest_verification: Most recent verification record (optional)

    Returns:
        Preview dict safe to show to potential buyers.
    """
    preview = {
        "artifact_hash": artifact.hash,
        "version": artifact.version,
        "domain": {
            "category": artifact.domain.category,
            "subcategory": artifact.domain.subcategory,
            "scope": artifact.domain.scope,
        },
        "knowledge_summary": {
            "format": artifact.knowledge.format,
            "sections": artifact.knowledge.sections,
            "token_count": artifact.knowledge.token_count,
            # NO content field — this is the whole point
        },
        "provenance": {
            "model": artifact.provenance.model,
            "training_rounds": artifact.provenance.training_rounds,
            "training_items_count": len(artifact.provenance.training_items),
            "created_at": artifact.provenance.created_at,
            # agent_id omitted for privacy
        },
        "attestation": {
            "expert_avg_error": artifact.attestation.expert_avg_error,
            "transfer_efficiency_pct": artifact.attestation.transfer_efficiency_pct,
            "eval_items_count": artifact.attestation.eval_items_count,
            "trials": artifact.attestation.trials,
        },
    }

    if trust_data:
        preview["trust"] = {
            "current_score": trust_data.get("current_score"),
            "verification_count": trust_data.get("verification_count", 0),
            "feedback_count": trust_data.get("feedback_count", 0),
            "last_updated": trust_data.get("last_updated"),
        }

    if latest_verification:
        preview["latest_verification"] = {
            "transfer_efficiency_pct": latest_verification.get("transfer_efficiency"),
            "adversarial_score": latest_verification.get("adversarial_score"),
            "trust_score": latest_verification.get("trust_score"),
            "created_at": latest_verification.get("created_at"),
        }

    return preview


def format_preview(preview: dict) -> str:
    """Format a preview dict for terminal display."""
    lines = [
        "=" * 60,
        "ARTIFACT PREVIEW",
        "=" * 60,
        f"  Hash: {preview['artifact_hash'][:16]}...",
        f"  Domain: {preview['domain']['category']}:{preview['domain']['subcategory']}",
        f"  Format: {preview['knowledge_summary']['format']}",
        f"  Sections: {', '.join(preview['knowledge_summary']['sections'])}",
        f"  Token count: {preview['knowledge_summary']['token_count']}",
        "",
        "  PROVENANCE",
        f"    Model: {preview['provenance']['model']}",
        f"    Training rounds: {preview['provenance']['training_rounds']}",
        f"    Training items: {preview['provenance']['training_items_count']}",
        f"    Created: {preview['provenance']['created_at'][:10]}",
        "",
        "  ATTESTATION (self-reported)",
        f"    Expert avg error: {preview['attestation']['expert_avg_error']:.2f}",
        f"    Transfer efficiency: {preview['attestation']['transfer_efficiency_pct']:.1f}%",
        f"    Eval items: {preview['attestation']['eval_items_count']}",
        f"    Trials: {preview['attestation']['trials']}",
    ]

    if "trust" in preview:
        t = preview["trust"]
        lines.extend([
            "",
            "  TRUST (independently verified)",
            f"    Trust score: {t['current_score']}/100",
            f"    Verifications: {t['verification_count']}",
            f"    Buyer feedback: {t['feedback_count']}",
        ])

    if "latest_verification" in preview:
        v = preview["latest_verification"]
        lines.extend([
            "",
            "  LATEST VERIFICATION",
            f"    Transfer efficiency: {v['transfer_efficiency_pct']:.1f}%",
            f"    Adversarial score: {v['adversarial_score']:.1f}/100",
            f"    Trust score: {v['trust_score']:.1f}/100",
            f"    Date: {v['created_at'][:10]}",
        ])

    lines.append("=" * 60)
    return "\n".join(lines)
