"""Tests for Phase A-C new features (no API calls required)."""

import sqlite3
from amm.domains import get_domain, list_domains
from amm.domains.defi_risk import DeFiRiskDomain
from amm.domains.cybersec import CyberSecDomain
from amm.benchmark.sandbox import bootstrap_ci, compute_transfer_efficiency, AssessmentResult
from amm.adversarial.runner import run_all_probes
from amm.config import ADVERSARIAL_RISK_WARN_CEILING
from amm.registry.db import init_db, store_artifact
from amm.marketplace.identity import create_identity, verify_ownership, register_participant, get_participant
from amm.marketplace.listing import create_listing, search_listings, get_listing, delist
from amm.marketplace.preview import generate_preview, format_preview
from amm.artifact.schema import (
    MemoryArtifact, ArtifactDomain, ArtifactKnowledge,
    ArtifactProvenance, ArtifactAttestation,
)


def _make_artifact(content="Test content", domain="DeFi", sub="risk-assessment"):
    return MemoryArtifact(
        domain=ArtifactDomain(category=domain, subcategory=sub),
        knowledge=ArtifactKnowledge(format="markdown", content=content, sections=["calibration", "heuristics"], token_count=100),
        provenance=ArtifactProvenance(agent_id="test-001", model="test-model", training_rounds=20, training_items=["A", "B"]),
        attestation=ArtifactAttestation(expert_avg_error=3.0, transfer_efficiency_pct=90.0, eval_items_count=8, trials=3),
    )


def _make_results(errors):
    return [
        AssessmentResult(protocol=f"p{i}", agent_score=50+e, true_score=50, error=e, reasoning="", confidence="high", red_flags=[])
        for i, e in enumerate(errors)
    ]


# --- A1: Domain registry ---

def test_domain_registry_list():
    domains = list_domains()
    assert "defi" in domains
    assert "cybersec" in domains


def test_domain_registry_get():
    d = get_domain("defi")
    assert isinstance(d, DeFiRiskDomain)
    d2 = get_domain("cybersec")
    assert isinstance(d2, CyberSecDomain)


def test_domain_registry_invalid():
    try:
        get_domain("nonexistent")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


# --- A2: Training rounds ---

def test_domain_training_rounds():
    d = get_domain("defi")
    assert d.training_rounds == 20


# --- A3: Bootstrap CI ---

def test_bootstrap_ci_basic():
    novice = [10.0, 12.0, 8.0, 15.0, 9.0]
    buyer = [3.0, 4.0, 2.0, 5.0, 3.0]
    lower, upper = bootstrap_ci(novice, buyer, n_bootstrap=500)
    assert lower > 0
    assert upper > lower
    assert upper <= 100


def test_bootstrap_ci_in_metrics():
    novice = _make_results([10, 12, 8, 15, 9])
    buyer = _make_results([3, 4, 2, 5, 3])
    metrics = compute_transfer_efficiency(novice, buyer)
    assert "confidence_interval_95" in metrics
    ci = metrics["confidence_interval_95"]
    assert len(ci) == 2
    assert ci[0] <= ci[1]


# --- A4: Negative TE threshold ---

def test_warn_threshold_lowered():
    assert ADVERSARIAL_RISK_WARN_CEILING == 50


# --- B1: Expanded DeFi corpus ---

def test_defi_corpus_size():
    d = get_domain("defi")
    assert len(d.get_all_items()) == 32
    assert len(d.get_training_items()) == 20
    assert len(d.get_held_out_items()) == 12
    assert len(d.get_scenarios()) == 8
    assert len(d.get_trap_items()) == 6


def test_defi_score_range():
    d = get_domain("defi")
    scores = [item.true_score for item in d.get_all_items()]
    assert min(scores) >= 0
    assert max(scores) <= 100
    # Good distribution
    assert min(scores) <= 20
    assert max(scores) >= 80


def test_defi_all_items_have_descriptions():
    d = get_domain("defi")
    for item in d.get_all_items():
        assert len(item.description) > 50, f"{item.name} has short description"
        assert item.name, f"Item missing name"


# --- C1: Marketplace tables ---

def test_marketplace_tables_created():
    conn = init_db(":memory:")
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    table_names = [t["name"] for t in tables]
    assert "participants" in table_names
    assert "listings" in table_names
    assert "purchases" in table_names
    conn.close()


# --- C2: Identity ---

def test_create_identity():
    identity = create_identity("Alice")
    assert identity["display_name"] == "Alice"
    assert len(identity["id"]) == 16
    assert len(identity["public_key_hex"]) == 64
    assert len(identity["secret_key_hex"]) == 64


def test_verify_ownership():
    identity = create_identity("Bob")
    assert verify_ownership(identity, identity["id"])
    assert not verify_ownership(identity, "wrong-id")


def test_register_and_get_participant():
    conn = init_db(":memory:")
    identity = create_identity("Charlie")
    register_participant(conn, identity)
    p = get_participant(conn, identity["id"])
    assert p is not None
    assert p["display_name"] == "Charlie"
    conn.close()


# --- C3: Listings ---

def test_create_and_search_listing():
    conn = init_db(":memory:")
    identity = create_identity("Seller")
    register_participant(conn, identity)
    artifact = _make_artifact()
    store_artifact(conn, artifact, seller_id=identity["id"])

    listing_id = create_listing(
        conn, artifact.hash, identity["id"],
        "DeFi Risk Artifact", "Expert-calibrated risk assessment", 5.0,
    )
    assert listing_id

    results = search_listings(conn)
    assert len(results) == 1
    assert results[0]["title"] == "DeFi Risk Artifact"
    assert results[0]["price_usd"] == 5.0

    conn.close()


def test_search_listings_filters():
    conn = init_db(":memory:")
    identity = create_identity("Seller")
    register_participant(conn, identity)

    a1 = _make_artifact("content1")
    a2 = _make_artifact("content2")
    store_artifact(conn, a1, seller_id=identity["id"])
    store_artifact(conn, a2, seller_id=identity["id"])

    create_listing(conn, a1.hash, identity["id"], "Cheap", "", 2.0)
    create_listing(conn, a2.hash, identity["id"], "Expensive", "", 8.0)

    cheap = search_listings(conn, max_price=5.0)
    assert len(cheap) == 1
    assert cheap[0]["title"] == "Cheap"

    conn.close()


def test_delist():
    conn = init_db(":memory:")
    identity = create_identity("Seller")
    register_participant(conn, identity)
    artifact = _make_artifact()
    store_artifact(conn, artifact)

    lid = create_listing(conn, artifact.hash, identity["id"], "Test", "", 1.0)
    assert delist(conn, lid, identity["id"])

    results = search_listings(conn)
    assert len(results) == 0
    conn.close()


# --- C4: Preview ---

def test_generate_preview():
    artifact = _make_artifact("SECRET KNOWLEDGE CONTENT")
    preview = generate_preview(artifact)

    # Should NOT contain the knowledge content
    assert "SECRET KNOWLEDGE CONTENT" not in str(preview)
    # Should contain metadata
    assert preview["domain"]["category"] == "DeFi"
    assert preview["knowledge_summary"]["token_count"] == 100
    assert "content" not in preview["knowledge_summary"]
    assert preview["attestation"]["transfer_efficiency_pct"] == 90.0


def test_format_preview():
    artifact = _make_artifact("SECRET")
    preview = generate_preview(artifact)
    text = format_preview(preview)
    assert "ARTIFACT PREVIEW" in text
    assert "SECRET" not in text
    assert "DeFi" in text
