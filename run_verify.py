#!/usr/bin/env python3
"""Verify a memory artifact.

Usage:
    export ANTHROPIC_API_KEY=your-key
    python run_verify.py --artifact path/to/artifact.json
    python run_verify.py --artifact-md path/to/artifact.md  # wrap raw markdown
"""

import argparse
import json
import sys
from pathlib import Path

from amm.api import create_client
from amm.config import MODEL
from amm.artifact.schema import MemoryArtifact
from amm.artifact.export import wrap_existing_artifact
from amm.domains import get_domain, list_domains
from amm.verification.referee import verify_artifact
from amm.registry.db import init_db, store_artifact, store_verification, get_trust_score
from amm.registry.trust import format_trust_report


def main():
    parser = argparse.ArgumentParser(description="Verify a memory artifact")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--artifact", type=str, help="Path to artifact JSON file")
    group.add_argument("--artifact-md", type=str, help="Path to raw markdown artifact")
    parser.add_argument("--domain", type=str, default="defi", choices=list_domains(), help="Domain to use")
    parser.add_argument("--model", type=str, default=MODEL, help="Model to use")
    parser.add_argument("--db", type=str, default=None, help="Registry DB path")
    parser.add_argument("--no-store", action="store_true", help="Don't store results in registry")

    args = parser.parse_args()
    domain = get_domain(args.domain)

    # Load artifact
    if args.artifact:
        with open(args.artifact) as f:
            data = json.load(f)
        artifact = MemoryArtifact.from_dict(data)
    else:
        with open(args.artifact_md) as f:
            content = f.read()
        artifact = wrap_existing_artifact(content, domain, model=args.model)

    print(f"Artifact hash: {artifact.hash}")
    print(f"Domain: {artifact.domain.category}:{artifact.domain.subcategory}")
    print(f"Knowledge: {artifact.knowledge.token_count} tokens")
    print(f"Training items: {artifact.provenance.training_items}")
    print()

    # Validate
    issues = artifact.validate()
    if issues:
        print(f"Validation issues: {issues}")
        sys.exit(1)

    # Verify
    print("Running verification protocol...")
    print("  Step 1: Artifact validated")
    print("  Steps 2-5: Running benchmark (novice + referee)...")

    client = create_client()
    certificate = verify_artifact(
        artifact=artifact,
        domain=domain,
        client=client,
        model=args.model,
    )

    # Print results
    print()
    print("=" * 60)
    print("VERIFICATION CERTIFICATE")
    print("=" * 60)
    print(f"  Certificate ID: {certificate.id}")
    print(f"  Transfer Efficiency: {certificate.results['transfer_efficiency_pct']:.1f}%")
    print(f"  Buyer Avg Error: {certificate.results['buyer_avg_error']:.2f}")
    print(f"  Novice Avg Error: {certificate.results['novice_avg_error']:.2f}")
    print()
    print("  ADVERSARIAL PROBES")
    print(f"    Bias:        {certificate.adversarial['bias_score']:.1f}/100")
    print(f"    Consistency: {certificate.adversarial['consistency_score']:.1f}/100")
    print(f"    Stego:       {certificate.adversarial['stego_score']:.1f}/100")
    print(f"    Overfit:     {certificate.adversarial['overfit_score']:.1f}/100")
    print(f"    Aggregate:   {certificate.adversarial['aggregate_score']:.1f}/100")
    print(f"    Verdict:     {certificate.adversarial['verdict']}")
    print()
    print(f"  TRUST SCORE: {certificate.trust_score:.1f}/100")
    print(f"  Expires: {certificate.expires_at[:10]}")
    print("=" * 60)

    if certificate.adversarial.get("flags"):
        print()
        print("FLAGS:")
        for flag in certificate.adversarial["flags"]:
            print(f"  ! {flag}")

    # Store in registry
    if not args.no_store:
        conn = init_db(args.db)
        store_artifact(conn, artifact)
        store_verification(conn, certificate)
        trust = get_trust_score(conn, artifact.hash)
        if trust:
            print()
            print(f"Registry updated. Trust score: {trust['current_score']}/100")
        conn.close()

    # Save certificate
    cert_path = Path("verification-certificate.json")
    with open(cert_path, "w") as f:
        f.write(certificate.to_json())
    print(f"\nCertificate saved to {cert_path}")


if __name__ == "__main__":
    main()
