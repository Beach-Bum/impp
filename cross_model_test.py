#!/usr/bin/env python3
"""Generate prompts for manual cross-model testing via ChatGPT.

Exports:
1. The system prompt (with or without artifact)
2. Individual protocol assessment prompts
3. Ground truth scores for comparison

Usage:
    python cross_model_test.py --domain defi --artifact path/to/artifact.json
    python cross_model_test.py --domain defi --novice  # no artifact (baseline)

Paste the output into ChatGPT, collect scores, then run:
    python cross_model_test.py --score --results path/to/results.json
"""

import argparse
import json
import sys
from pathlib import Path

from amm.domains import get_domain, list_domains
from amm.artifact.schema import MemoryArtifact


def generate_prompts(domain_name: str, artifact_path: str | None = None):
    """Generate copy-pasteable prompts for ChatGPT testing."""
    domain = get_domain(domain_name)
    all_items = domain.get_all_items()

    # Load artifact if provided
    artifact_content = None
    if artifact_path:
        with open(artifact_path) as f:
            data = json.load(f)
        artifact = MemoryArtifact.from_dict(data)
        artifact_content = artifact.knowledge.content

    # System prompt
    if artifact_content:
        system = domain.get_buyer_system_prompt(artifact_content)
        mode = "BUYER (with artifact)"
    else:
        system = domain.get_assessment_system_prompt()
        mode = "NOVICE (no artifact)"

    print("=" * 70)
    print(f"CROSS-MODEL TEST — {mode}")
    print(f"Domain: {domain.name}")
    print(f"Items: {len(all_items)}")
    print("=" * 70)
    print()
    print("STEP 1: Paste this SYSTEM PROMPT into ChatGPT as your first message:")
    print("-" * 70)
    print(system)
    print("-" * 70)
    print()
    print("STEP 2: For each protocol below, paste it as a follow-up message.")
    print("        Record the score from ChatGPT's JSON response.")
    print()

    # Ground truth reference (for you, not for ChatGPT)
    ground_truth = {}
    for i, item in enumerate(all_items, 1):
        ground_truth[item.name] = item.true_score
        prompt = domain.get_assessment_user_prompt(item)
        print(f"--- PROTOCOL {i}/{len(all_items)}: {item.name} ---")
        print(prompt)
        print()

    print("=" * 70)
    print("GROUND TRUTH (do NOT show to ChatGPT):")
    print("-" * 70)
    for name, score in sorted(ground_truth.items(), key=lambda x: x[1]):
        print(f"  {score:3d} — {name}")
    print("=" * 70)

    # Save ground truth for scoring
    gt_path = Path(f"ground-truth-{domain_name}.json")
    with open(gt_path, "w") as f:
        json.dump(ground_truth, f, indent=2)
    print(f"\nGround truth saved to {gt_path}")
    print(f"\nAfter collecting ChatGPT scores, create a JSON file like:")
    print(f'  {{"AlphaLend": 28, "YieldMaxi": 75, ...}}')
    print(f"Then run: python cross_model_test.py --score --results <file>.json --domain {domain_name}")


def score_results(results_path: str, domain_name: str):
    """Score ChatGPT results against ground truth."""
    domain = get_domain(domain_name)
    all_items = domain.get_all_items()
    ground_truth = {item.name: item.true_score for item in all_items}

    with open(results_path) as f:
        gpt_scores = json.load(f)

    print("=" * 70)
    print("CROSS-MODEL SCORING")
    print("=" * 70)

    errors = []
    for name, true_score in sorted(ground_truth.items()):
        if name not in gpt_scores:
            print(f"  MISSING: {name}")
            continue
        gpt_score = gpt_scores[name]
        error = abs(gpt_score - true_score)
        errors.append(error)
        marker = "✓" if error <= 5 else "~" if error <= 10 else "✗"
        print(f"  {marker} {name:20s}  GPT: {gpt_score:3d}  True: {true_score:3d}  Error: {error:2d}")

    if not errors:
        print("No scores to evaluate.")
        return

    avg_error = sum(errors) / len(errors)

    # Compare against expected novice baseline
    # DeFi novice avg error ~7.4 (original 8 items), CyberSec ~18.0
    print()
    print(f"  Items scored: {len(errors)}/{len(ground_truth)}")
    print(f"  Average error: {avg_error:.2f}")
    print()

    # If we have a novice baseline, compute TE
    novice_path = Path(f"novice-baseline-{domain_name}.json")
    if novice_path.exists():
        with open(novice_path) as f:
            novice_data = json.load(f)
        novice_avg = novice_data.get("avg_error", 0)
        if novice_avg > 0:
            te = (novice_avg - avg_error) / novice_avg * 100
            print(f"  Novice baseline avg error: {novice_avg:.2f}")
            print(f"  Transfer efficiency: {te:.1f}%")
    else:
        print(f"  (Run novice baseline first to compute transfer efficiency)")
        print(f"  Save as: {novice_path}")

    print("=" * 70)

    # Save results
    output = {
        "domain": domain_name,
        "model": "gpt-chatgpt-manual",
        "avg_error": round(avg_error, 2),
        "item_count": len(errors),
        "per_item": {
            name: {"gpt_score": gpt_scores.get(name), "true_score": ground_truth[name], "error": abs(gpt_scores.get(name, 0) - ground_truth[name])}
            for name in ground_truth if name in gpt_scores
        },
    }
    out_path = Path(f"cross-model-results-{domain_name}.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Results saved to {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Cross-model testing via ChatGPT")
    parser.add_argument("--domain", type=str, default="defi", choices=list_domains())
    parser.add_argument("--artifact", type=str, default=None, help="Path to artifact JSON (buyer mode)")
    parser.add_argument("--novice", action="store_true", help="Generate novice prompts (no artifact)")
    parser.add_argument("--score", action="store_true", help="Score collected results")
    parser.add_argument("--results", type=str, help="Path to ChatGPT results JSON")

    args = parser.parse_args()

    if args.score:
        if not args.results:
            print("--results required with --score")
            sys.exit(1)
        score_results(args.results, args.domain)
    else:
        generate_prompts(args.domain, args.artifact)


if __name__ == "__main__":
    main()
