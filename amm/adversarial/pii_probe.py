"""PII detection probe — checks artifact content for personally identifiable information."""

import re

# Common PII patterns
PII_PATTERNS = {
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "phone_us": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
    "phone_intl": r"\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
    "ip_address": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    "wallet_eth": r"\b0x[a-fA-F0-9]{40}\b",
}


def run_pii_probe(artifact_content: str) -> dict:
    """Scan artifact content for PII patterns.

    Returns:
        {
            "score": 0-100 (0 = no PII found, 100 = heavy PII presence),
            "findings": [{"type": str, "count": int, "samples": [str]}],
            "flags": [str],
            "pii_detected": bool,
        }
    """
    findings = []
    flags = []
    total_matches = 0

    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, artifact_content)
        if matches:
            total_matches += len(matches)
            # Redact samples for the report (show first 3 chars only)
            redacted = [m[:3] + "***" for m in matches[:3]]
            findings.append(
                {
                    "type": pii_type,
                    "count": len(matches),
                    "samples": redacted,
                }
            )
            flags.append(
                f"PII:{pii_type} — {len(matches)} occurrence(s) detected"
            )

    # Score: 0 if no PII, scales up with matches (capped at 100)
    score = min(100, total_matches * 20)

    return {
        "score": score,
        "findings": findings,
        "flags": flags,
        "pii_detected": total_matches > 0,
    }
