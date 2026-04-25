"""Trust score computation utilities."""

from datetime import datetime, timezone, timedelta


def compute_freshness_pct(
    created_at: str,
    half_life_days: int = 180,
) -> float:
    """Compute freshness as a percentage (0-100).

    Uses exponential decay with configurable half-life.
    An artifact at half_life_days old has 50% freshness.

    Args:
        created_at: ISO 8601 timestamp
        half_life_days: Days until freshness drops to 50%

    Returns:
        Freshness percentage (0-100).
    """
    created = datetime.fromisoformat(created_at)
    now = datetime.now(timezone.utc)

    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)

    age_days = (now - created).total_seconds() / 86400

    if age_days <= 0:
        return 100.0

    # Exponential decay: freshness = 100 * (0.5 ^ (age / half_life))
    import math
    freshness = 100.0 * math.pow(0.5, age_days / half_life_days)

    return round(max(0, min(100, freshness)), 1)


def format_trust_report(trust_data: dict, verifications: list[dict]) -> str:
    """Format a human-readable trust report."""
    lines = [
        "=" * 60,
        "TRUST REPORT",
        "=" * 60,
        f"Artifact Hash: {trust_data.get('artifact_hash', 'N/A')}",
        f"Current Trust Score: {trust_data.get('current_score', 'N/A')}/100",
        f"Verifications: {trust_data.get('verification_count', 0)}",
        f"Buyer Feedback: {trust_data.get('feedback_count', 0)}",
        f"Last Updated: {trust_data.get('last_updated', 'N/A')}",
        "",
    ]

    if verifications:
        lines.append("VERIFICATION HISTORY")
        lines.append("-" * 40)
        for v in verifications:
            lines.append(
                f"  [{v.get('created_at', 'N/A')[:10]}] "
                f"TE: {v.get('transfer_efficiency', 0):.1f}% | "
                f"Adversarial: {v.get('adversarial_score', 0):.1f} | "
                f"Trust: {v.get('trust_score', 0):.1f}"
            )

    lines.append("=" * 60)
    return "\n".join(lines)
