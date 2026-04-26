#!/usr/bin/env python3
"""Orchestrator for IMPP paper v1 experiments.

Usage:
    python experiments/run_paper_v1.py --dry-run          # validate setup only
    python experiments/run_paper_v1.py --domain defi_risk  # run one domain
    python experiments/run_paper_v1.py --trials 3          # full run

Requires:
    ANTHROPIC_API_KEY  — for Claude-based conditions
    OPENAI_API_KEY     — for cross-model conditions (optional)

Conditions run per domain:
    1. no_memory          — baseline, no artifact attached
    2. raw_context         — full artifact text dumped into context
    3. prompt_skill_file   — structured prompt-only skill file (no IMPP metadata)
    4. impp_artifact        — full IMPP artifact with declared attach mode
    5. retrieval_only      — RAG-style retrieval from artifact chunks
    6. few_shot            — few-shot examples extracted from artifact
    7. negative_transfer   — artifact from wrong domain (cybersec → defi or vice versa)
    8. poisoned_artifact   — deliberately manipulated artifact

Each condition is evaluated on the domain's task set. Results are appended to
data/paper_v1/results_v2.csv with columns:
    run_id,domain,model,condition,attach_mode,task_id,score,error,cost_usd,latency_ms,is_sample
"""

import argparse
import csv
import json
import sys
import time
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "paper_v1"
RESULTS_FILE = DATA_DIR / "results_v2.csv"

CONDITIONS = [
    "no_memory",
    "raw_context",
    "prompt_skill_file",
    "impp_artifact",
    "retrieval_only",
    "few_shot",
    "negative_transfer",
    "poisoned_artifact",
]

RESULT_COLUMNS = [
    "run_id", "domain", "model", "condition", "attach_mode",
    "task_id", "score", "error", "cost_usd", "latency_ms", "is_sample",
]


def load_tasks(domain: str) -> list[dict]:
    tasks = []
    with open(DATA_DIR / "tasks.jsonl") as f:
        for line in f:
            task = json.loads(line)
            if task["domain"] == domain:
                tasks.append(task)
    return tasks


def load_labels() -> dict[str, float]:
    labels = {}
    with open(DATA_DIR / "labels_public_sample.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            labels[row["item_id"]] = float(row["true_score"])
    return labels


def validate_setup(domain: str) -> bool:
    """Check that all required files exist and parse correctly."""
    ok = True
    for name in ["tasks.jsonl", "labels_public_sample.csv", "splits.json",
                  "artifacts_sanitized.jsonl"]:
        path = DATA_DIR / name
        if not path.exists():
            print(f"MISSING: {path}")
            ok = False
        else:
            print(f"OK: {path}")

    tasks = load_tasks(domain)
    labels = load_labels()
    print(f"Tasks for {domain}: {len(tasks)}")
    print(f"Labels loaded: {len(labels)}")

    # Check all tasks have labels
    missing = [t["item_id"] for t in tasks if t["item_id"] not in labels]
    if missing:
        print(f"WARNING: {len(missing)} tasks missing labels: {missing[:5]}")
        ok = False

    return ok


def run_condition(domain: str, condition: str, model: str, tasks: list[dict],
                  labels: dict, trial: int, dry_run: bool) -> list[dict]:
    """Run a single experimental condition. Returns result rows."""
    run_id = f"{domain}_{condition}_t{trial}_{int(time.time())}"
    results = []

    for task in tasks:
        if dry_run:
            # Stub: would call LLM here
            score = labels.get(task["item_id"], 50.0)
            error = 0.0
            cost = 0.0
            latency = 0.0
        else:
            # TODO: wire up actual LLM calls via amm.benchmark
            raise NotImplementedError(
                f"Live experiment execution not yet wired. "
                f"Use --dry-run to validate setup, or run run_experiment.py "
                f"for the legacy single-condition runner."
            )

        results.append({
            "run_id": run_id,
            "domain": domain,
            "model": model,
            "condition": condition,
            "attach_mode": _attach_mode_for_condition(condition),
            "task_id": task["item_id"],
            "score": score,
            "error": error,
            "cost_usd": cost,
            "latency_ms": latency,
            "is_sample": True,
        })

    return results


def _attach_mode_for_condition(condition: str) -> str:
    mapping = {
        "no_memory": "none",
        "raw_context": "prepend_policy",
        "prompt_skill_file": "prepend_policy",
        "impp_artifact": "prepend_policy",
        "retrieval_only": "retrieval_only",
        "few_shot": "few_shot_examples",
        "negative_transfer": "prepend_policy",
        "poisoned_artifact": "prepend_policy",
    }
    return mapping.get(condition, "unknown")


def write_results(results: list[dict]) -> None:
    file_exists = RESULTS_FILE.exists()
    with open(RESULTS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=RESULT_COLUMNS)
        if not file_exists:
            writer.writeheader()
        writer.writerows(results)
    print(f"Wrote {len(results)} rows to {RESULTS_FILE}")


def main():
    parser = argparse.ArgumentParser(description="IMPP paper v1 experiment orchestrator")
    parser.add_argument("--domain", default="defi_risk",
                        choices=["defi_risk", "cybersec_vuln"],
                        help="Domain to evaluate")
    parser.add_argument("--trials", type=int, default=3, help="Number of trials")
    parser.add_argument("--model", default="claude-sonnet-4-20250514",
                        help="Model to use")
    parser.add_argument("--conditions", nargs="+", default=CONDITIONS,
                        help="Conditions to run")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate setup without running experiments")
    args = parser.parse_args()

    # Map domain arg to data domain key
    domain_key = "defi" if args.domain == "defi_risk" else "cybersec"

    print(f"IMPP Paper v1 Experiment Runner")
    print(f"Domain: {args.domain} (data key: {domain_key})")
    print(f"Model: {args.model}")
    print(f"Trials: {args.trials}")
    print(f"Conditions: {args.conditions}")
    print(f"Dry run: {args.dry_run}")
    print()

    if not validate_setup(domain_key):
        print("\nSetup validation failed. Fix issues above before running.")
        sys.exit(1)

    if args.dry_run:
        print("\n--dry-run: setup validated. No experiments executed.")
        return

    tasks = load_tasks(domain_key)
    labels = load_labels()
    all_results = []

    for trial in range(1, args.trials + 1):
        for condition in args.conditions:
            print(f"\n--- Trial {trial}, Condition: {condition} ---")
            results = run_condition(
                domain_key, condition, args.model, tasks, labels, trial,
                dry_run=args.dry_run,
            )
            all_results.extend(results)

    if all_results:
        write_results(all_results)

    print(f"\nDone. Total rows: {len(all_results)}")


if __name__ == "__main__":
    main()
