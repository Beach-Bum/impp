#!/usr/bin/env python3
"""Orchestrator for IMPP paper v1 experiments.

Usage:
    python experiments/run_paper_v1.py --dry-run                    # validate setup only
    python experiments/run_paper_v1.py --dry-run --domain defi_risk # validate one domain

    python experiments/run_paper_v1.py --live --domain defi_risk \
        --conditions no_memory impp_artifact --trials 1             # real API calls

Requires (for --live):
    ANTHROPIC_API_KEY  — for --provider anthropic (default)
    GOOGLE_API_KEY     — for --provider gemini

Conditions:
    1. no_memory          — baseline, no artifact attached
    2. raw_context         — full artifact text dumped into context
    3. prompt_skill_file   — structured prompt-only skill file (no IMPP metadata)
    4. impp_artifact        — full IMPP artifact with declared attach mode
    5. retrieval_only      — RAG-style retrieval from artifact chunks
    6. few_shot            — few-shot examples extracted from artifact
    7. negative_transfer   — artifact from wrong domain (cybersec → defi or vice versa)
    8. poisoned_artifact   — deliberately manipulated artifact

Output:
    --dry-run  → no output file (validation only)
    --live     → appends to data/paper_v1/results_real.csv (is_sample=false)

Sample fixtures in data/paper_v1/results.csv are never modified.
"""

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "paper_v1"
REAL_RESULTS_FILE = DATA_DIR / "results_real.csv"

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

LIVE_SUPPORTED = {"no_memory", "impp_artifact"}

REAL_RESULT_COLUMNS = [
    "run_id", "created_at", "domain", "model", "condition", "attach_mode",
    "task_id", "predicted_score", "label", "error",
    "cost_usd", "latency_ms", "is_sample", "notes",
]

PROVIDER_ENV_VARS = {
    "anthropic": {"ANTHROPIC_API_KEY": "Required for Claude-based conditions"},
    "gemini": {"GOOGLE_API_KEY": "Required for Gemini-based conditions"},
    "openai": {"OPENAI_API_KEY": "Required for OpenAI-based conditions"},
}

PROVIDER_DEFAULT_MODELS = {
    "anthropic": "claude-sonnet-4-20250514",
    "gemini": "gemini-2.5-flash",
    "openai": "gpt-4o",
}


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


def load_artifact(domain: str) -> dict | None:
    """Load the first matching non-adversarial artifact for a domain."""
    domain_map = {"defi": "defi_risk", "cybersec": "cybersec_vuln"}
    target = domain_map.get(domain, domain)
    with open(DATA_DIR / "artifacts_sanitized.jsonl") as f:
        for line in f:
            artifact = json.loads(line)
            if artifact.get("is_sample") and not artifact.get("is_adversarial"):
                scope = artifact.get("scope", {})
                if scope.get("domain") == target:
                    return artifact
    return None


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

    missing = [t["item_id"] for t in tasks if t["item_id"] not in labels]
    if missing:
        print(f"WARNING: {len(missing)} tasks missing labels: {missing[:5]}")
        ok = False

    return ok


def check_live_env(provider: str) -> list[str]:
    """Check that required env vars are set for live mode. Returns missing vars."""
    required = PROVIDER_ENV_VARS.get(provider, {})
    missing = []
    for var, desc in required.items():
        if not os.environ.get(var):
            missing.append(f"  {var}: {desc}")
    return missing


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


def _create_llm_client(provider: str, model: str):
    """Create an LLMClient for the given provider. Late import to avoid amm at dry-run."""
    os.environ.setdefault("AMM_TESTING", "1")
    if provider == "gemini":
        from amm.api_base import LLMClient
        import json as _json
        import urllib.request
        import urllib.error
        from amm.config import API_RETRY_ATTEMPTS, API_RETRY_BASE_DELAY

        class GeminiClient(LLMClient):
            """Gemini via Google's native generateContent API."""
            def __init__(self, model_name: str):
                self.model = model_name
                self._api_key = os.environ["GOOGLE_API_KEY"]

            def call(self, system: str, user_message: str, max_tokens: int = 400) -> str:
                url = (
                    f"https://generativelanguage.googleapis.com/v1beta/"
                    f"models/{self.model}:generateContent?key={self._api_key}"
                )
                payload = _json.dumps({
                    "system_instruction": {"parts": [{"text": system}]},
                    "contents": [{"parts": [{"text": user_message}]}],
                    "generationConfig": {
                        "maxOutputTokens": max_tokens,
                        "thinkingConfig": {"thinkingBudget": 0},
                    },
                }).encode("utf-8")
                headers = {"Content-Type": "application/json"}
                for attempt in range(API_RETRY_ATTEMPTS):
                    try:
                        req = urllib.request.Request(url, data=payload, headers=headers)
                        with urllib.request.urlopen(req, timeout=120) as resp:
                            data = _json.loads(resp.read().decode("utf-8"))
                        return data["candidates"][0]["content"]["parts"][0]["text"]
                    except (urllib.error.URLError, urllib.error.HTTPError, KeyError):
                        if attempt < API_RETRY_ATTEMPTS - 1:
                            time.sleep(API_RETRY_BASE_DELAY * (2 ** attempt))
                            continue
                        raise

        return GeminiClient(model)
    else:
        from amm.api import create_llm_client
        return create_llm_client(provider=provider, model=model)


def run_condition_live(domain: str, condition: str, model: str,
                       tasks: list[dict], labels: dict, trial: int,
                       provider: str = "anthropic") -> list[dict]:
    """Live run: make real API calls via amm.benchmark.sandbox."""
    if condition not in LIVE_SUPPORTED:
        raise NotImplementedError(
            f"Condition '{condition}' is not yet implemented for --live. "
            f"Supported: {sorted(LIVE_SUPPORTED)}"
        )

    # Late import so --dry-run never touches amm (which needs AMM_JWT_SECRET)
    os.environ.setdefault("AMM_TESTING", "1")
    from amm.domains import get_domain
    from amm.benchmark.sandbox import evaluate_agent_llm

    domain_name_map = {"defi": "defi", "cybersec": "cybersec"}
    amm_domain = get_domain(domain_name_map.get(domain, domain))
    llm_client = _create_llm_client(provider, model)

    # Filter to paper fixture task IDs for reproducibility
    paper_task_ids = {t["item_id"] for t in tasks}
    all_items = amm_domain.get_all_items()
    items = [item for item in all_items if item.name in paper_task_ids]
    matched_ids = {item.name for item in items}
    missing_ids = paper_task_ids - matched_ids
    if missing_ids:
        preview = sorted(missing_ids)[:5]
        raise RuntimeError(
            f"{len(missing_ids)} paper fixture task IDs not found in "
            f"amm_domain.get_all_items(): {preview}"
        )
    print(f"    Matched {len(items)}/{len(paper_task_ids)} paper fixture items "
          f"(domain has {len(all_items)} total)")

    run_id = f"live_{domain}_{condition}_t{trial}_{int(time.time())}"
    now = datetime.now(timezone.utc).isoformat()

    if condition == "no_memory":
        print(f"    Evaluating novice baseline ({len(items)} items)...")
        t0 = time.time()
        agent_results = evaluate_agent_llm(
            llm_client, amm_domain, items=items,
        )
        elapsed_ms = (time.time() - t0) * 1000

    elif condition == "impp_artifact":
        artifact = load_artifact(domain)
        if not artifact:
            raise RuntimeError(f"No artifact found for domain '{domain}'")
        artifact_text = artifact.get("summary", "")
        print(f"    Evaluating with IMPP artifact ({len(items)} items)...")
        print(f"    Artifact: {artifact.get('name')} v{artifact.get('version')}")
        system_prompt = amm_domain.get_buyer_system_prompt(artifact_text)
        t0 = time.time()
        agent_results = evaluate_agent_llm(
            llm_client, amm_domain, items=items,
            system_prompt_override=system_prompt,
        )
        elapsed_ms = (time.time() - t0) * 1000

    else:
        raise NotImplementedError(f"Condition '{condition}' not implemented for --live")

    # Build result rows
    results = []
    for ar in agent_results:
        true_score = labels.get(ar.protocol, ar.true_score)
        results.append({
            "run_id": run_id,
            "created_at": now,
            "domain": domain,
            "model": model,
            "condition": condition,
            "attach_mode": _attach_mode_for_condition(condition),
            "task_id": ar.protocol,
            "predicted_score": ar.agent_score,
            "label": true_score,
            "error": abs(ar.agent_score - true_score),
            "cost_usd": 0.0,  # TODO: extract from API response
            "latency_ms": round(elapsed_ms / len(agent_results), 1),
            "is_sample": False,
            "notes": "",
        })

    return results


def write_real_results(results: list[dict]) -> None:
    """Append results to results_real.csv. Creates header if file is empty/new."""
    file_exists = REAL_RESULTS_FILE.exists()
    with open(REAL_RESULTS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=REAL_RESULT_COLUMNS)
        if not file_exists:
            writer.writeheader()
        writer.writerows(results)
    print(f"Appended {len(results)} rows to {REAL_RESULTS_FILE}")


def print_run_manifest(args, domain_key: str, live: bool, output_file: Path | None,
                       total_rows: int) -> None:
    """Print a run summary to stdout."""
    print()
    print("=" * 60)
    print("RUN MANIFEST")
    print("=" * 60)
    print(f"  run_id:      {domain_key}_{int(time.time())}")
    print(f"  domain:      {args.domain} (data key: {domain_key})")
    print(f"  model:       {args.model}")
    print(f"  conditions:  {args.conditions}")
    print(f"  trials:      {args.trials}")
    print(f"  live:        {live}")
    print(f"  output_file: {output_file or 'none (dry-run)'}")
    print(f"  total_rows:  {total_rows}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="IMPP paper v1 experiment orchestrator")
    parser.add_argument("--domain", default="defi_risk",
                        choices=["defi_risk", "cybersec_vuln"],
                        help="Domain to evaluate")
    parser.add_argument("--trials", type=int, default=3, help="Number of trials")
    parser.add_argument("--provider", default="anthropic",
                        choices=["anthropic", "gemini", "openai"],
                        help="API provider (default: anthropic)")
    parser.add_argument("--model", default=None,
                        help="Model to use (defaults per provider)")
    parser.add_argument("--conditions", nargs="+", default=CONDITIONS,
                        help="Conditions to run")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true",
                      help="Validate setup without running experiments (default-safe)")
    mode.add_argument("--live", action="store_true",
                      help="Execute real API calls. Requires ANTHROPIC_API_KEY.")
    args = parser.parse_args()

    # Safety: if neither --dry-run nor --live, default to dry-run
    if not args.dry_run and not args.live:
        args.dry_run = True
        print("NOTE: Neither --dry-run nor --live specified. Defaulting to --dry-run.\n")

    # Resolve model default per provider
    if args.model is None:
        args.model = PROVIDER_DEFAULT_MODELS.get(args.provider, "claude-sonnet-4-20250514")

    # Map domain arg to data domain key
    domain_key = "defi" if args.domain == "defi_risk" else "cybersec"

    print("IMPP Paper v1 Experiment Runner")
    print(f"Domain: {args.domain} (data key: {domain_key})")
    print(f"Provider: {args.provider}")
    print(f"Model: {args.model}")
    print(f"Trials: {args.trials}")
    print(f"Conditions: {args.conditions}")
    print(f"Mode: {'--live' if args.live else '--dry-run'}")
    print()

    if not validate_setup(domain_key):
        print("\nSetup validation failed. Fix issues above before running.")
        sys.exit(1)

    if args.dry_run:
        print("\n--dry-run: setup validated. No experiments executed.")
        print_run_manifest(args, domain_key, live=False, output_file=None, total_rows=0)
        return

    # Live mode checks
    if args.live:
        missing = check_live_env(args.provider)
        if missing:
            print("\nERROR: Missing required environment variables for --live:")
            for m in missing:
                print(m)
            print("\nSet them and retry, or use --dry-run to validate without API calls.")
            sys.exit(1)

        # Check for unsupported conditions
        unsupported = [c for c in args.conditions if c not in LIVE_SUPPORTED]
        if unsupported:
            print(f"\nERROR: These conditions are not yet implemented for --live: {unsupported}")
            print(f"Supported: {sorted(LIVE_SUPPORTED)}")
            print("Remove unsupported conditions or use --dry-run.")
            sys.exit(1)

    tasks = load_tasks(domain_key)
    labels = load_labels()
    all_results = []

    for trial in range(1, args.trials + 1):
        for condition in args.conditions:
            print(f"\n--- Trial {trial}, Condition: {condition} ---")
            results = run_condition_live(
                domain_key, condition, args.model, tasks, labels, trial,
                provider=args.provider,
            )
            all_results.extend(results)

            avg_error = sum(r["error"] for r in results) / len(results) if results else 0
            print(f"    Items: {len(results)}, Avg error: {avg_error:.2f}")

    if all_results:
        write_real_results(all_results)

    print_run_manifest(args, domain_key, live=True,
                       output_file=REAL_RESULTS_FILE, total_rows=len(all_results))


if __name__ == "__main__":
    main()
