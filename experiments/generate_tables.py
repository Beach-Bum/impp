#!/usr/bin/env python3
"""Generate summary tables from IMPP paper v1 experiment data.

Usage:
    python experiments/generate_tables.py

Reads from data/paper_v1/ and prints LaTeX-ready tables to stdout.
"""

import csv
import json
import statistics
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "paper_v1"


def load_results() -> list[dict]:
    rows = []
    with open(DATA_DIR / "results.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def print_same_model_table(results: list[dict]) -> None:
    print("=" * 70)
    print("Table 1: Same-Model Transfer Results (3 trials)")
    print("=" * 70)
    print(f"{'Domain':<12} {'Trial':<6} {'Expert ε':<10} {'Novice ε':<10} {'Buyer ε':<10} {'TE %':<8}")
    print("-" * 70)

    for domain in ["defi", "cybersec"]:
        domain_rows = [r for r in results if r["experiment"] == "same_model" and r["domain"] == domain]
        te_values = []
        for r in domain_rows:
            te = float(r["transfer_efficiency_pct"])
            te_values.append(te)
            print(f"{domain:<12} {r['trial']:<6} {r['expert_avg_error']:<10} {r['novice_avg_error']:<10} {r['buyer_avg_error']:<10} {te:<8.1f}")

        if te_values:
            mean_te = statistics.mean(te_values)
            std_te = statistics.stdev(te_values) if len(te_values) > 1 else 0
            print(f"{domain:<12} {'avg':<6} {'':10} {'':10} {'':10} {mean_te:.1f} ± {std_te:.1f}")
        print()


def print_cross_model_table(results: list[dict]) -> None:
    print("=" * 70)
    print("Table 2: Cross-Model Transfer (Claude Sonnet → GPT-4o)")
    print("=" * 70)
    print(f"{'Condition':<30} {'Items':<8} {'Avg Error':<12}")
    print("-" * 70)

    conditions = [
        ("cross_model_novice", "GPT-4o novice (no artifact)"),
        ("cross_model_full", "GPT-4o + full artifact"),
        ("cross_model_sanitized", "GPT-4o + sanitized artifact"),
    ]
    for exp, label in conditions:
        rows = [r for r in results if r["experiment"] == exp]
        for r in rows:
            print(f"{label:<30} {r['item_count']:<8} {r['buyer_avg_error']:<12}")
    print()


def print_adversarial_table() -> None:
    with open(DATA_DIR / "adversarial_results.json") as f:
        adv = json.load(f)

    print("=" * 70)
    print("Table 3: Adversarial Probe Results (Poisoned Artifact)")
    print("=" * 70)
    scores = adv["adversarial_scores"]
    print(f"{'Probe':<20} {'Score':<8}")
    print("-" * 30)
    for probe, score in scores.items():
        if probe != "aggregate_score":
            print(f"{probe:<20} {score:<8}")
    print(f"{'AGGREGATE':<20} {scores['aggregate_score']:<8}")
    print(f"\nVerdict: {adv['verdict']}")
    print(f"Trust score: {adv['trust_score']}")
    print(f"Transfer efficiency: {adv['transfer_results']['transfer_efficiency_pct']}%")
    print(f"Flags: {len(adv['flags'])}")
    print()


def print_summary() -> None:
    results = load_results()

    # Same-model DeFi
    defi_te = [float(r["transfer_efficiency_pct"]) for r in results
               if r["experiment"] == "same_model" and r["domain"] == "defi"]
    # Same-model CyberSec
    cyber_te = [float(r["transfer_efficiency_pct"]) for r in results
                if r["experiment"] == "same_model" and r["domain"] == "cybersec"]

    print("=" * 70)
    print("Summary Statistics")
    print("=" * 70)
    print(f"DeFi same-model TE:    {statistics.mean(defi_te):.1f}% ± {statistics.stdev(defi_te):.1f}% (n=3 trials, 8 items)")
    print(f"CyberSec same-model TE: {statistics.mean(cyber_te):.1f}% ± {statistics.stdev(cyber_te):.1f}% (n=3 trials, 8 items)")
    print(f"Cross-model (full):    avg_error=5.19 (32 items, manual GPT-4o)")
    print(f"Cross-model (sanitized): avg_error=6.03 (32 items)")
    print(f"Cross-model (novice):  avg_error=6.00 (32 items)")
    print(f"Poisoned artifact TE:  -39.0% (detected, trust_score=35.8)")
    print()


if __name__ == "__main__":
    results = load_results()
    print_same_model_table(results)
    print_cross_model_table(results)
    print_adversarial_table()
    print_summary()
