#!/usr/bin/env python3
"""Generate markdown tables for the IMPP paper from experiment data.

Usage:
    python experiments/generate_paper_tables.py                  # sample tables (default)
    python experiments/generate_paper_tables.py --source sample  # same as above
    python experiments/generate_paper_tables.py --source real    # from results_real.csv

Reads from data/paper_v1/ and writes markdown files to paper/tables/ (sample)
or paper/tables/real/ (real).
"""

import argparse
import csv
import json
import statistics
import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "paper_v1"
TABLES_DIR = Path(__file__).parent.parent / "paper" / "tables"


SAMPLE_BANNER = (
    "> **SAMPLE TABLE** — generated from synthetic/sample fixtures. "
    "Do not cite as final empirical evidence."
)


def load_results() -> list[dict]:
    rows = []
    with open(DATA_DIR / "results.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def load_real_results() -> list[dict]:
    path = DATA_DIR / "results_real.csv"
    if not path.exists():
        print(f"ERROR: {path} does not exist.")
        sys.exit(1)
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    if not rows:
        print(f"ERROR: {path} is header-only. Run experiments with --live first.")
        sys.exit(1)
    sample_rows = [r for r in rows if r.get("is_sample", "").lower() == "true"]
    if sample_rows:
        print(f"ERROR: {path} contains {len(sample_rows)} rows with is_sample=true. "
              "Real tables must not include sample data.")
        sys.exit(1)
    return rows


def has_sample_rows(results: list[dict]) -> bool:
    return any(r.get("is_sample", "").lower() == "true" for r in results)


def generate_same_model_table(results: list[dict]) -> str:
    """Table 1: Same-model transfer efficiency across domains and trials."""
    lines = []
    if has_sample_rows(results):
        lines.extend([SAMPLE_BANNER, ""])
    lines.extend([
        "## Table 1: Same-Model Transfer Results",
        "",
        "| Domain | Trial | Expert MAE | Novice MAE | Artifact MAE | TE (%) |",
        "|--------|-------|-----------|-----------|-------------|--------|",
    ])

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
    lines = []
    if has_sample_rows(results):
        lines.extend([SAMPLE_BANNER, ""])
    lines.extend([
        "## Table 2: Cross-Model Transfer (Claude Sonnet -> GPT-4o)",
        "",
        "| Condition | Items | Avg Error |",
        "|-----------|-------|-----------|",
    ])

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
    lines = [SAMPLE_BANNER, ""]
    lines.extend([
        "## Table 3: Adversarial Probe Results (Poisoned Artifact)",
        "",
        "| Probe | Score |",
        "|-------|-------|",
    ])

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

    lines = []
    if has_sample_rows(results):
        lines.extend([SAMPLE_BANNER, ""])
    lines.extend([
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
    ])
    return "\n".join(lines)


def generate_real_condition_table(results: list[dict]) -> str:
    """Table: Per-condition MAE from real experiment runs."""
    lines = [
        "## Table: Condition Comparison (Real Runs)",
        "",
        "| Domain | Condition | Items | MAE | Trials |",
        "|--------|-----------|-------|-----|--------|",
    ]

    for domain in ["defi", "cybersec"]:
        domain_rows = [r for r in results if r["domain"] == domain]
        conditions = sorted(set(r["condition"] for r in domain_rows))
        for condition in conditions:
            cond_rows = [r for r in domain_rows if r["condition"] == condition]
            run_ids = sorted(set(r["run_id"] for r in cond_rows))
            trial_maes = []
            for run_id in run_ids:
                run_rows = [r for r in cond_rows if r["run_id"] == run_id]
                mae = statistics.mean(float(r["error"]) for r in run_rows)
                trial_maes.append(mae)
            overall_mae = statistics.mean(trial_maes)
            items = len([r for r in cond_rows if r["run_id"] == run_ids[0]])
            lines.append(
                f"| {domain} | {condition} | {items} | {overall_mae:.2f} | {len(run_ids)} |"
            )

    lines.append("")
    lines.append("*MAE = mean absolute error averaged across trials. "
                 "Each trial evaluates the paper fixture task set.*")
    return "\n".join(lines)


def generate_real_summary_table(results: list[dict]) -> str:
    """Summary statistics from real experiment runs."""
    lines = [
        "## Summary Statistics (Real Runs)",
        "",
        "| Metric | Value |",
        "|--------|-------|",
    ]

    for domain in ["defi", "cybersec"]:
        domain_rows = [r for r in results if r["domain"] == domain]
        conditions = sorted(set(r["condition"] for r in domain_rows))
        for condition in conditions:
            cond_rows = [r for r in domain_rows if r["condition"] == condition]
            run_ids = sorted(set(r["run_id"] for r in cond_rows))
            trial_maes = []
            for run_id in run_ids:
                run_rows = [r for r in cond_rows if r["run_id"] == run_id]
                mae = statistics.mean(float(r["error"]) for r in run_rows)
                trial_maes.append(mae)
            mean_mae = statistics.mean(trial_maes)
            std_mae = statistics.stdev(trial_maes) if len(trial_maes) > 1 else 0
            items = len([r for r in cond_rows if r["run_id"] == run_ids[0]])
            lines.append(
                f"| {domain} / {condition} MAE | {mean_mae:.2f} +/- {std_mae:.2f} "
                f"(n={len(run_ids)}, {items} items) |"
            )

    # TE if both no_memory and impp_artifact exist for a domain
    for domain in ["defi", "cybersec"]:
        domain_rows = [r for r in results if r["domain"] == domain]
        conditions = set(r["condition"] for r in domain_rows)
        if "no_memory" in conditions and "impp_artifact" in conditions:
            novice_rows = [r for r in domain_rows if r["condition"] == "no_memory"]
            artifact_rows = [r for r in domain_rows if r["condition"] == "impp_artifact"]
            novice_mae = statistics.mean(float(r["error"]) for r in novice_rows)
            artifact_mae = statistics.mean(float(r["error"]) for r in artifact_rows)
            if novice_mae > 0:
                te = ((novice_mae - artifact_mae) / novice_mae) * 100
                lines.append(f"| {domain} TE (novice→artifact) | {te:.1f}% |")

    lines.append("")
    lines.append("*TE = transfer efficiency = (novice_MAE - artifact_MAE) / novice_MAE x 100. "
                 "Positive TE means the artifact improved performance over novice baseline.*")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate IMPP paper tables")
    parser.add_argument("--source", default="sample", choices=["sample", "real"],
                        help="Data source: sample fixtures or real experiment results")
    args = parser.parse_args()

    if args.source == "sample":
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

    elif args.source == "real":
        real_dir = TABLES_DIR / "real"
        real_dir.mkdir(parents=True, exist_ok=True)
        results = load_real_results()

        tables = {
            "conditions.md": generate_real_condition_table(results),
            "summary.md": generate_real_summary_table(results),
        }

        for filename, content in tables.items():
            path = real_dir / filename
            path.write_text(content + "\n")
            print(f"Wrote {path}")
            print(content)
            print()


if __name__ == "__main__":
    main()
