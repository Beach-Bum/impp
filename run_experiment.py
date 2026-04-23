#!/usr/bin/env python3
"""Full end-to-end pipeline: train → export → verify → store.

Usage:
    export ANTHROPIC_API_KEY=your-key
    python run_experiment.py --trials 3
"""

import argparse
import json
import sys
from pathlib import Path

from amm.api import create_client, create_llm_client
from amm.config import MODEL
from amm.domains import get_domain, list_domains
from amm.benchmark.engine import run_benchmark, run_cross_model_benchmark
from amm.verification.referee import verify_artifact
from amm.registry.db import init_db, store_artifact, store_verification, get_trust_score


def main():
    parser = argparse.ArgumentParser(description="Full memory market experiment")
    parser.add_argument("--trials", type=int, default=1, help="Number of trials")
    parser.add_argument("--domain", type=str, default="defi", choices=list_domains(), help="Domain to use")
    parser.add_argument("--model", type=str, default=MODEL, help="Model to use")
    parser.add_argument("--buyer-provider", type=str, default=None,
                        choices=["openai", "ollama"],
                        help="Evaluate buyer on a different provider (cross-model transfer)")
    parser.add_argument("--buyer-model", type=str, default=None,
                        help="Model name for buyer provider (default: gpt-4o for openai, llama3 for ollama)")
    parser.add_argument("--db", type=str, default=None, help="Registry DB path")
    parser.add_argument("--output", type=str, default="experiment-results.json", help="Output file")

    args = parser.parse_args()
    domain = get_domain(args.domain)
    client = create_client()
    conn = init_db(args.db)

    # Cross-model setup
    buyer_llm = None
    if args.buyer_provider:
        buyer_llm = create_llm_client(
            provider=args.buyer_provider,
            model=args.buyer_model or "",
        )

    all_trial_results = []

    for trial in range(args.trials):
        print(f"\n{'='*60}")
        print(f"TRIAL {trial + 1}/{args.trials}")
        print(f"{'='*60}")

        # Phase 1: Train + Evaluate
        rounds = domain.training_rounds
        print(f"\nPhase 1: Training expert ({rounds} rounds) + evaluation...")
        if buyer_llm:
            print(f"  Cross-model: training on {args.model}, buyer on {args.buyer_provider}:{buyer_llm.model}")
            bench_run = run_cross_model_benchmark(client, domain, args.model, buyer_llm)
        else:
            bench_run = run_benchmark(client, domain, args.model)

        print(f"  Expert avg error: {bench_run.metrics['expert_avg_error']:.2f}")
        print(f"  Novice avg error: {bench_run.metrics['novice_avg_error']:.2f}")
        print(f"  Buyer avg error:  {bench_run.metrics['buyer_avg_error']:.2f}")
        print(f"  Transfer efficiency: {bench_run.metrics.get('relative_transfer_efficiency_pct', bench_run.metrics['transfer_efficiency_pct']):.1f}%")

        # Phase 2: Verify the artifact
        print("\nPhase 2: Running verification protocol...")
        certificate = verify_artifact(
            artifact=bench_run.artifact,
            domain=domain,
            client=client,
            model=args.model,
            novice_cache=bench_run.novice_results,
        )

        print(f"  Adversarial score: {certificate.adversarial['aggregate_score']:.1f}")
        print(f"  Verdict: {certificate.adversarial['verdict']}")
        print(f"  Trust score: {certificate.trust_score:.1f}/100")

        # Phase 3: Store
        store_artifact(conn, bench_run.artifact)
        store_verification(conn, certificate)

        trial_result = {
            "trial": trial + 1,
            "metrics": bench_run.metrics,
            "artifact_hash": bench_run.artifact.hash,
            "certificate_id": certificate.id,
            "adversarial": {
                "aggregate": certificate.adversarial["aggregate_score"],
                "bias": certificate.adversarial["bias_score"],
                "consistency": certificate.adversarial["consistency_score"],
                "stego": certificate.adversarial["stego_score"],
                "overfit": certificate.adversarial["overfit_score"],
                "verdict": certificate.adversarial["verdict"],
            },
            "trust_score": certificate.trust_score,
        }
        all_trial_results.append(trial_result)

    # Summary
    print(f"\n{'='*60}")
    print("EXPERIMENT SUMMARY")
    print(f"{'='*60}")

    avg_te = sum(
        t["metrics"].get("relative_transfer_efficiency_pct", t["metrics"]["transfer_efficiency_pct"])
        for t in all_trial_results
    ) / len(all_trial_results)

    avg_trust = sum(t["trust_score"] for t in all_trial_results) / len(all_trial_results)
    avg_adversarial = sum(t["adversarial"]["aggregate"] for t in all_trial_results) / len(all_trial_results)

    verdicts = [t["adversarial"]["verdict"] for t in all_trial_results]

    print(f"  Trials: {args.trials}")
    print(f"  Avg Transfer Efficiency: {avg_te:.1f}%")
    print(f"  Avg Trust Score: {avg_trust:.1f}/100")
    print(f"  Avg Adversarial Score: {avg_adversarial:.1f}/100")
    print(f"  Verdicts: {verdicts}")

    # Save results
    metadata = {
        "model": args.model,
        "trials": args.trials,
        "domain": domain.name,
    }
    if args.buyer_provider:
        metadata["buyer_provider"] = args.buyer_provider
        metadata["buyer_model"] = buyer_llm.model

    output = {
        "metadata": metadata,
        "summary": {
            "avg_transfer_efficiency": round(avg_te, 1),
            "avg_trust_score": round(avg_trust, 1),
            "avg_adversarial_score": round(avg_adversarial, 1),
        },
        "trials": all_trial_results,
    }

    with open(args.output, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\nResults saved to {args.output}")
    conn.close()


if __name__ == "__main__":
    main()
