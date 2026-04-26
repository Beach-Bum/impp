#!/usr/bin/env python3
"""Generate markdown tables for the IMPP paper from experiment data.

Usage:
    python experiments/generate_paper_tables.py

Reads from data/paper_v1/ and writes markdown files to paper/tables/.
Also prints tables to stdout for quick inspection.
"""

import csv
import json
import statistics
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "paper_v1"
TABLES_DIR = Path(__file__).parent.parent / "paper" / "tables"


def load_results() -> list[dict]:
    rows = []
    with open(DATA_DIR / "results.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def generate_same_model_table(results: list[dict]) -> str:
    """Table 1: Same-model transfer efficiency across domains and trials."""
    lines = [
        "## Table 1: Same-Model Transfer Results",
        "",
        "| Domain | Trial | Expert MAE | Novice MAE | Artifact MAE | TE (%) |",
        "|--------|-------|-----------|-----------|-------------|--------|",
    ]

    for domain in ["defi", "cybersec"]:
        domain_rows = [r for r in results
                       if r["experiment"] == "same_model" and r["domain"] == domain]
        te_values = []
        for r in domain_rows:
            te = float(r["transfer_efficiency_pct"])
            te_values.append(te)
            lines.append(
                f"| {domain} | {r['trial']} | {r['expert_avg_error']} | "
                f"{r['novice_avg_error']} | {r['buyer_avg_error']} | {te:.1f} |"
            )

        if te_values:
            mean_te = statistics.mean(te_values)
            std_te = statistics.stdev(te_values) if len(te_values) > 1 else 0
            lines.append(f"| **{domain} avg** | | | | | **{mean_te:.1f} +/- {std_te:.1f}** |")
        lines.append("")

    lines.append("")
    lines.append("*Conditions: claude-sonnet-4, 8 synthetic items per domain, "
                 "3 independent trials. TE = (novice_error - artifact_error) / "
                 "(novice_error - expert_error) x 100.*")
    return "\n".join(lines)


def generate_cross_model_table(results: list[dict]) -> str:
    """Table 2: Cross-model transfer (Claude -> GPT-4o)."""
    lines = [
        "## Table 2: Cross-Model Transfer (Claude Sonnet -> GPT-4o)",
        "",
        "| Condition | Items | Avg Error |",
        "|-----------|-------|-----------|",
    ]

    conditions = [
        ("cross_model_novice", "GPT-4o novice (no artifact)"),
        ("cross_model_full", "GPT-4o + full artifact"),
        ("cross_model_sanitized", "GPT-4o + sanitized artifact"),
    ]
    for exp, label in conditions:
        rows = [r for r in results if r["experiment"] == exp]
        for r in rows:
            lines.append(f"| {label} | {r['item_count']} | {r['buyer_avg_error']} |")

    lines.append("")
    lines.append("*32 DeFi protocols (core + extended). Single trial, manual GPT-4o evaluation. "
                 "Cross-model transfer shows modest improvement over novice baseline.*")
    return "\n".join(lines)


def generate_adversarial_table() -> str:
    """Table 3: Adversarial detection results."""
    with open(DATA_DIR / "adversarial_results.json") as f:
        adv = json.load(f)

    scores = adv["adversarial_scores"]
    lines = [
        "## Table 3: Adversarial Probe Results (Poisoned Artifact)",
        "",
        "| Probe | Score |",
        "|-------|-------|",
    ]

    probe_labels = {
        "bias_score": "Bias detection",
        "consistency_score": "Consistency",
        "stego_score": "Steganography",
        "overfit_score": "Overfitting",
        "aggregate_score": "**Aggregate**",
    }
    for key, label in probe_labels.items():
        lines.append(f"| {label} | {scores[key]} |")

    lines.append("")
    lines.append(f"| Verdict | {adv['verdict']} |")
    lines.append(f"| Trust score | {adv['trust_score']} |")
    lines.append(f"| Transfer efficiency | {adv['transfer_results']['transfer_efficiency_pct']}% |")
    lines.append(f"| Flags raised | {len(adv['flags'])} |")
    lines.append("")
    lines.append("*Poisoned artifact deliberately underweights bridge risk. Negative TE (-39%) "
                 "confirms the artifact degrades performance below novice baseline. "
                 "Referee verdict WARN triggers rejection.*")
    return "\n".join(lines)


def generate_summary_table(results: list[dict]) -> str:
    """Summary statistics table."""
    defi_te = [float(r["transfer_efficiency_pct"]) for r in results
               if r["experiment"] == "same_model" and r["domain"] == "defi"]
    cyber_te = [float(r["transfer_efficiency_pct"]) for r in results
                if r["experiment"] == "same_model" and r["domain"] == "cybersec"]

    lines = [
        "## Summary Statistics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| DeFi same-model TE | {statistics.mean(defi_te):.1f}% +/- {statistics.stdev(defi_te):.1f}% (n=3, 8 items) |",
        f"| CyberSec same-model TE | {statistics.mean(cyber_te):.1f}% +/- {statistics.stdev(cyber_te):.1f}% (n=3, 8 items) |",
        f"| Cross-model full artifact | avg_error=5.19 (32 items) |",
        f"| Cross-model sanitized | avg_error=6.03 (32 items) |",
        f"| Cross-model novice | avg_error=6.00 (32 items) |",
        f"| Poisoned artifact TE | -39.0% (detected, trust_score=35.8) |",
        "",
        "*All results are pilot-scale on synthetic domains. Known limitations: "
        "small item counts, benchmark leakage risk from public labels, "
        "prompt/model variance across runs, incomplete negative-transfer testing, "
        "uncalibrated trust-score weights.*",
    ]
    return "\n".join(lines)


def main():
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    results = load_results()

    tables = {
        "table1_same_model.md": generate_same_model_table(results),
        "table2_cross_model.md": generate_cross_model_table(results),
        "table3_adversarial.md": generate_adversarial_table(),
        "summary.md": generate_summary_table(results),
    }

    for filename, content in tables.items():
        path = TABLES_DIR / filename
        path.write_text(content + "\n")
        print(f"Wrote {path}")
        print(content)
        print()


if __name__ == "__main__":
    main()
