#!/usr/bin/env python3
"""Seed the marketplace with realistic demo data.

Creates participants, artifacts, verification certificates, listings,
and feedback so the Carbon UI has real data to display.
"""

import json
import uuid
from datetime import datetime, timezone, timedelta

from amm.registry.db import (
    init_db, store_artifact, store_verification, add_buyer_feedback,
)
from amm.marketplace.identity import create_identity, register_participant
from amm.marketplace.listing import create_listing
from amm.artifact.schema import (
    MemoryArtifact, ArtifactDomain, ArtifactKnowledge,
    ArtifactProvenance, ArtifactAttestation,
)
from amm.verification.certificate import generate_certificate


def seed():
    conn = init_db()
    print("Seeding marketplace database...")

    # --- Participants ---
    sellers = [
        create_identity("Sentinel Labs"),
        create_identity("NeuroForge Research"),
        create_identity("Cipher Collective"),
        create_identity("Meridian AI"),
    ]
    buyers = [
        create_identity("Acme Corp"),
        create_identity("BlockShield DAO"),
    ]
    for p in sellers + buyers:
        register_participant(conn, p)
    print(f"  Created {len(sellers)} sellers, {len(buyers)} buyers")

    # --- Artifacts ---
    artifacts_data = [
        {
            "domain": ("DeFi", "risk-assessment"),
            "content": "# DeFi Risk Assessment Expert Artifact\n\nCalibration framework for DeFi protocol risk scoring...",
            "model": "claude-sonnet-4-20250514",
            "training_rounds": 20,
            "training_items": ["AlphaLend", "YieldMaxi", "StableSwap", "PerpDEX", "BridgeX"],
            "attestation": {"expert_avg_error": 3.3, "transfer_efficiency_pct": 92.2, "eval_items_count": 32, "trials": 3},
            "seller": sellers[0],
            "title": "DeFi Risk Calibration Pack v2.1",
            "description": "Expert-calibrated risk scoring for DeFi protocols. Trained on 20 protocols across lending, bridges, yield aggregators, and stablecoins. Cross-model validated on GPT-4o.",
            "price": 5.00,
        },
        {
            "domain": ("CyberSec", "vulnerability-assessment"),
            "content": "# Cybersecurity Vulnerability Assessment Artifact\n\nSeverity scoring framework calibrated on real CVEs...",
            "model": "claude-sonnet-4-20250514",
            "training_rounds": 20,
            "training_items": ["Log4Shell", "MOVEitTransfer", "ProxyShell", "CitrixBleed", "SolarWindsOrion"],
            "attestation": {"expert_avg_error": 3.9, "transfer_efficiency_pct": 95.5, "eval_items_count": 24, "trials": 3},
            "seller": sellers[1],
            "title": "CVE Severity Scorer v1.8",
            "description": "Vulnerability severity assessment trained on 16 real CVEs including Log4Shell, MOVEit, Zerologon. CVSS-anchored with operational context adjustment.",
            "price": 8.00,
        },
        {
            "domain": ("DeFi", "incident-triage"),
            "content": "# DeFi Incident Triage Memory\n\nFast triage decision framework for DeFi security incidents...",
            "model": "claude-sonnet-4-20250514",
            "training_rounds": 15,
            "training_items": ["FlashLoanAttack", "OracleManipulation", "RugPull", "BridgeExploit"],
            "attestation": {"expert_avg_error": 5.1, "transfer_efficiency_pct": 78.4, "eval_items_count": 16, "trials": 2},
            "seller": sellers[2],
            "title": "DeFi Incident Triage v1.7",
            "description": "Fast incident classification and response prioritization. Best for security ops teams. Higher negative transfer risk under adversarial conditions.",
            "price": 3.50,
        },
        {
            "domain": ("Research", "citation-analysis"),
            "content": "# Research Citation Memory\n\nCitation consistency and source verification framework...",
            "model": "claude-sonnet-4-20250514",
            "training_rounds": 20,
            "training_items": ["ArXivSearch", "ScholarVerify", "CitationChain", "SourceRanking"],
            "attestation": {"expert_avg_error": 4.2, "transfer_efficiency_pct": 85.0, "eval_items_count": 20, "trials": 3},
            "seller": sellers[3],
            "title": "Research Citation Memory v2.0",
            "description": "Improves citation accuracy and source verification in research synthesis workflows. Low negative transfer risk.",
            "price": 4.00,
        },
        {
            "domain": ("Support", "escalation"),
            "content": "# Fraud Escalation Memory Pack\n\nEscalation decision framework for ambiguous support cases...",
            "model": "claude-sonnet-4-20250514",
            "training_rounds": 25,
            "training_items": ["ChargebackDispute", "AccountTakeover", "SocialEngineering", "InsiderThreat", "PhishingReport"],
            "attestation": {"expert_avg_error": 2.8, "transfer_efficiency_pct": 94.1, "eval_items_count": 30, "trials": 5},
            "seller": sellers[0],
            "title": "Fraud Escalation Memory Pack v3.2",
            "description": "Improves escalation accuracy for ambiguous chargeback and support cases. Best on fintech stacks. Signed provenance, cross-model validated.",
            "price": 12.00,
        },
    ]

    created_artifacts = []
    for ad in artifacts_data:
        cat, sub = ad["domain"]
        artifact = MemoryArtifact(
            domain=ArtifactDomain(category=cat, subcategory=sub),
            knowledge=ArtifactKnowledge(
                format="markdown",
                content=ad["content"],
                sections=["calibration", "heuristics", "red_flags", "mitigants"],
                token_count=len(ad["content"].split()),
            ),
            provenance=ArtifactProvenance(
                agent_id=str(uuid.uuid4()),
                model=ad["model"],
                training_rounds=ad["training_rounds"],
                training_items=ad["training_items"],
            ),
            attestation=ArtifactAttestation(**ad["attestation"]),
        )
        store_artifact(conn, artifact, seller_id=ad["seller"]["id"])
        created_artifacts.append((artifact, ad))

    print(f"  Created {len(created_artifacts)} artifacts")

    # --- Verification Certificates ---
    for artifact, ad in created_artifacts:
        benchmark_info = {
            "id": str(uuid.uuid4()),
            "domain": f"{ad['domain'][0]}:{ad['domain'][1]}",
            "protocol_count": ad["attestation"]["eval_items_count"],
            "held_out_count": ad["attestation"]["eval_items_count"] // 3,
            "hash": str(uuid.uuid4())[:16],
        }
        te = ad["attestation"]["transfer_efficiency_pct"]
        results = {
            "buyer_avg_error": ad["attestation"]["expert_avg_error"] * 1.1,
            "novice_avg_error": ad["attestation"]["expert_avg_error"] * 3.5,
            "transfer_efficiency_pct": te,
            "per_protocol": {},
        }
        adversarial = {
            "aggregate_score": 12.0,
            "bias_score": 8.0,
            "consistency_score": 15.0,
            "stego_score": 5.0,
            "overfit_score": 18.0,
            "verdict": "PASS",
            "all_flags": [],
        }

        from amm.verification.referee import compute_trust_score
        trust = compute_trust_score(te, adversarial["aggregate_score"])

        cert = generate_certificate(
            artifact_hash=artifact.hash,
            benchmark_info=benchmark_info,
            results=results,
            adversarial=adversarial,
            trust_score=trust,
            referee_model="claude-sonnet-4-20250514",
        )
        store_verification(conn, cert)

    print(f"  Created {len(created_artifacts)} verification certificates")

    # --- Listings ---
    for artifact, ad in created_artifacts:
        create_listing(
            conn,
            artifact_hash=artifact.hash,
            seller_id=ad["seller"]["id"],
            title=ad["title"],
            description=ad["description"],
            price_usd=ad["price"],
            license_type="licensed",
            max_buyers=10,
        )

    print(f"  Created {len(created_artifacts)} listings")

    # --- Buyer feedback ---
    for artifact, ad in created_artifacts[:3]:
        add_buyer_feedback(
            conn,
            artifact_hash=artifact.hash,
            buyer_id=buyers[0]["id"],
            reported_improvement=ad["attestation"]["transfer_efficiency_pct"] * 0.9,
            rating=4,
            feedback_text="Solid improvement on our benchmarks.",
        )

    print(f"  Added feedback for 3 artifacts")

    # Summary
    print("\nDone. API server can now serve real data.")
    print(f"  Run: uvicorn api_server:app --reload --port 8100")
    conn.close()


if __name__ == "__main__":
    seed()
