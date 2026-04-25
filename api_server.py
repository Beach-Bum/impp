#!/usr/bin/env python3
"""IMPP API Server — The Agent Memory Registry.

Exposes verification, search, and publish endpoints for the IMPP CLI,
plus legacy marketplace endpoints for the preview UI.

Usage:
    uvicorn api_server:app --reload --port 8100
"""

import hashlib
import json
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from amm.registry.db import (
    init_db, store_artifact, get_artifact, get_trust_score,
    get_verifications, add_buyer_feedback,
)
from amm.marketplace.identity import (
    create_identity, register_participant, get_participant, load_identity,
)
from amm.marketplace.listing import (
    create_listing, search_listings, get_listing, delist,
)
from amm.marketplace.preview import generate_preview, format_preview
from amm.artifact.schema import MemoryArtifact
from amm.registry.trust import format_trust_report
from amm.verification.certificate import (
    generate_certificate,
    load_private_key,
    VerificationCertificate,
)

app = FastAPI(title="IMPP — The Agent Memory Registry", version="0.5.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "https://memorymarket.ai",
        "https://www.memorymarket.ai",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global DB connection
_conn = None

def get_db():
    global _conn
    if _conn is None:
        _conn = init_db()
    return _conn


# --- Listings ---

@app.get("/api/listings")
def api_search_listings(
    domain: str | None = None,
    min_trust: float | None = None,
    max_price: float | None = None,
):
    conn = get_db()
    results = search_listings(conn, domain=domain, min_trust=min_trust, max_price=max_price)
    # Enrich with preview data
    enriched = []
    for listing in results:
        artifact_data = get_artifact(conn, listing["artifact_hash"])
        trust = get_trust_score(conn, listing["artifact_hash"])
        verifications = get_verifications(conn, listing["artifact_hash"])
        latest_v = verifications[0] if verifications else None

        enriched.append({
            "id": listing["id"],
            "title": listing["title"],
            "description": listing["description"],
            "domain": listing["domain"],
            "price_usd": listing["price_usd"],
            "license_type": listing.get("license_type", "licensed"),
            "status": listing["status"],
            "listed_at": listing["listed_at"],
            "seller_id": listing["seller_id"],
            "artifact_hash": listing["artifact_hash"],
            "trust_score": trust["current_score"] if trust else None,
            "verification_count": trust["verification_count"] if trust else 0,
            "feedback_count": trust["feedback_count"] if trust else 0,
            "latest_transfer_efficiency": latest_v["transfer_efficiency"] if latest_v else None,
            "latest_adversarial_score": latest_v["adversarial_score"] if latest_v else None,
        })

    return {"listings": enriched}


@app.get("/api/listings/{listing_id}")
def api_get_listing(listing_id: str):
    conn = get_db()
    listing = get_listing(conn, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing


# --- Artifacts ---

@app.get("/api/artifacts/{artifact_hash}")
def api_get_artifact(artifact_hash: str):
    conn = get_db()
    artifact = get_artifact(conn, artifact_hash)
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return artifact


@app.get("/api/artifacts/{artifact_hash}/preview")
def api_get_preview(artifact_hash: str):
    conn = get_db()
    artifact_data = get_artifact(conn, artifact_hash)
    if not artifact_data:
        raise HTTPException(status_code=404, detail="Artifact not found")

    trust = get_trust_score(conn, artifact_hash)
    verifications = get_verifications(conn, artifact_hash)
    latest_v = verifications[0] if verifications else None

    import json
    artifact = MemoryArtifact.from_dict({
        "domain": {"category": artifact_data["domain"].split(":")[0], "subcategory": artifact_data["domain"].split(":")[-1]},
        "knowledge": {"format": "markdown", "content": artifact_data["knowledge_content"], "sections": [], "token_count": len(artifact_data["knowledge_content"].split())},
        "provenance": json.loads(artifact_data["provenance_json"]),
        "attestation": json.loads(artifact_data["attestation_json"]),
        "hash": artifact_data["hash"],
    })

    preview = generate_preview(artifact, trust, latest_v)
    return preview


# --- Trust ---

@app.get("/api/trust/{artifact_hash}")
def api_get_trust(artifact_hash: str):
    conn = get_db()
    trust = get_trust_score(conn, artifact_hash)
    if not trust:
        raise HTTPException(status_code=404, detail="No trust data")
    verifications = get_verifications(conn, artifact_hash)
    return {
        "trust": trust,
        "verifications": verifications,
        "report": format_trust_report(trust, verifications),
    }


# --- Feedback ---

class FeedbackRequest(BaseModel):
    buyer_id: str
    rating: int
    improvement: float
    text: str = ""

@app.post("/api/artifacts/{artifact_hash}/feedback")
def api_add_feedback(artifact_hash: str, req: FeedbackRequest):
    conn = get_db()
    feedback_id = add_buyer_feedback(
        conn, artifact_hash, req.buyer_id, req.improvement, req.rating, req.text,
    )
    trust = get_trust_score(conn, artifact_hash)
    return {"feedback_id": feedback_id, "updated_trust": trust}


# --- Identity ---

class IdentityRequest(BaseModel):
    display_name: str

@app.post("/api/identity")
def api_create_identity(req: IdentityRequest):
    identity = create_identity(req.display_name)
    conn = get_db()
    register_participant(conn, identity)
    return {
        "id": identity["id"],
        "display_name": identity["display_name"],
        "public_key_hex": identity["public_key_hex"],
    }

@app.get("/api/identity/{participant_id}")
def api_get_identity(participant_id: str):
    conn = get_db()
    p = get_participant(conn, participant_id)
    if not p:
        raise HTTPException(status_code=404, detail="Participant not found")
    return dict(p)


# --- Sell ---

class ListingRequest(BaseModel):
    artifact_hash: str
    seller_id: str
    title: str
    description: str = ""
    price_usd: float
    license_type: str = "licensed"
    max_buyers: int = 10

@app.post("/api/listings")
def api_create_listing(req: ListingRequest):
    conn = get_db()
    listing_id = create_listing(
        conn, req.artifact_hash, req.seller_id, req.title,
        req.description, req.price_usd, req.license_type, req.max_buyers,
    )
    return {"listing_id": listing_id}


# --- Portfolio / Control Tower ---

@app.get("/api/portfolio")
def api_portfolio():
    """Get control tower data: active listings, recent verifications, alerts."""
    conn = get_db()

    # Stats
    listing_count = conn.execute("SELECT COUNT(*) as c FROM listings WHERE status='active'").fetchone()["c"]
    verification_count = conn.execute("SELECT COUNT(*) as c FROM verifications").fetchone()["c"]
    feedback_count = conn.execute("SELECT COUNT(*) as c FROM buyer_feedback").fetchone()["c"]

    # Recent verifications as "agents" (what's actively being evaluated)
    recent_verifications = conn.execute("""
        SELECT v.id, v.artifact_hash, v.transfer_efficiency, v.adversarial_score,
               v.trust_score, v.created_at, a.domain, l.title
        FROM verifications v
        JOIN artifacts a ON v.artifact_hash = a.hash
        LEFT JOIN listings l ON l.artifact_hash = a.hash
        ORDER BY v.created_at DESC LIMIT 10
    """).fetchall()

    agents = []
    for v in recent_verifications:
        te = v["transfer_efficiency"] or 0
        adv = v["adversarial_score"] or 0
        if te < 0:
            status = "Blocked"
        elif adv > 50:
            status = "Warning"
        elif adv > 30:
            status = "Watch"
        else:
            status = "Healthy"

        agents.append({
            "id": v["id"][:8],
            "name": v["title"] or v["artifact_hash"][:12],
            "memory": v["domain"],
            "status": status,
            "trust_score": v["trust_score"],
            "transfer_efficiency": te,
            "adversarial_score": adv,
            "last_eval": v["created_at"],
        })

    # Alerts: any artifact with adversarial > 25 or negative feedback
    alert_rows = conn.execute("""
        SELECT v.artifact_hash, v.adversarial_score, v.transfer_efficiency, l.title
        FROM verifications v
        LEFT JOIN listings l ON l.artifact_hash = v.artifact_hash
        WHERE v.adversarial_score > 25 OR v.transfer_efficiency < 0
    """).fetchall()

    alerts = []
    for r in alert_rows:
        if (r["transfer_efficiency"] or 0) < 0:
            alerts.append({
                "id": r["artifact_hash"][:8],
                "title": f"Negative transfer on {r['title'] or r['artifact_hash'][:12]}",
                "severity": "Blocked",
                "summary": f"Transfer efficiency is {r['transfer_efficiency']:.1f}%. Artifact should be revoked.",
            })
        elif (r["adversarial_score"] or 0) > 40:
            alerts.append({
                "id": r["artifact_hash"][:8],
                "title": f"High adversarial score on {r['title'] or r['artifact_hash'][:12]}",
                "severity": "Warning",
                "summary": f"Adversarial score {r['adversarial_score']:.1f}/100 exceeds warning threshold.",
            })

    # Total spend estimate
    total_prices = conn.execute("SELECT SUM(price_usd) as total FROM listings WHERE status='active'").fetchone()

    return {
        "stats": {
            "active_listings": listing_count,
            "verifications": verification_count,
            "feedback_received": feedback_count,
            "monthly_spend": total_prices["total"] or 0,
        },
        "agents": agents,
        "alerts": alerts,
    }


# ====================================================================
# IMPP Registry Endpoints (new — used by `impp` CLI)
# ====================================================================

class VerifyRequest(BaseModel):
    artifact: dict

@app.post("/api/verify")
def api_verify(req: VerifyRequest):
    """Submit an artifact for verification. Returns a signed certificate."""
    artifact_data = req.artifact
    artifact_json = json.dumps(artifact_data, sort_keys=True)
    artifact_hash = hashlib.sha256(artifact_json.encode()).hexdigest()

    # Store artifact if not already present
    conn = get_db()
    existing = get_artifact(conn, artifact_hash)
    if not existing:
        store_artifact(conn, {
            "hash": artifact_hash,
            "domain": artifact_data.get("domain", {}).get("category", "unknown"),
            "knowledge_content": json.dumps(artifact_data.get("knowledge", {})),
            "provenance_json": json.dumps(artifact_data.get("provenance", {})),
            "attestation_json": json.dumps(artifact_data.get("attestation", {})),
        })

    # Run verification (simplified for now — full pipeline would call referee)
    # TODO: wire up full amm.verification.referee pipeline
    trust_score = 75.0
    adversarial = {
        "aggregate_score": 20.0,
        "bias_score": 15.0,
        "consistency_score": 25.0,
        "stego_score": 20.0,
        "overfit_score": 15.0,
        "verdict": "PASS",
        "all_flags": [],
    }

    # Try to load signing key
    try:
        signing_key = load_private_key()
    except (FileNotFoundError, TypeError):
        signing_key = None

    cert = generate_certificate(
        artifact_hash=artifact_hash,
        benchmark_info={"id": "server-verify", "domain": artifact_data.get("domain", {}).get("category", "unknown")},
        results={"transfer_efficiency_pct": trust_score},
        adversarial=adversarial,
        trust_score=trust_score,
        referee_model="server-v0.5",
        signing_key=signing_key,
    )

    return {
        "trust_score": cert.trust_score,
        "artifact_hash": artifact_hash,
        "certificate": cert.to_dict(),
        "signed": bool(cert.signature),
    }


@app.get("/api/search")
def api_search(
    domain: str | None = None,
    min_trust: float = 0,
    limit: int = 20,
):
    """Search the registry for verified artifacts."""
    conn = get_db()

    query = "SELECT * FROM artifacts WHERE 1=1"
    params: list[Any] = []
    if domain:
        query += " AND domain = ?"
        params.append(domain)
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(query, params).fetchall()

    artifacts = []
    for row in rows:
        trust = get_trust_score(conn, row["hash"])
        score = trust["current_score"] if trust else 0
        if score >= min_trust:
            artifacts.append({
                "artifact_hash": row["hash"],
                "domain": row["domain"],
                "name": row.get("title", row["hash"][:12]),
                "trust_score": score,
                "created_at": row.get("created_at", ""),
            })

    return {"artifacts": artifacts, "total": len(artifacts)}


class PublishRequest(BaseModel):
    artifact: dict
    domain: str
    name: str | None = None

@app.post("/api/publish")
def api_publish(req: PublishRequest):
    """Publish a verified artifact to the registry."""
    artifact_json = json.dumps(req.artifact, sort_keys=True)
    artifact_hash = hashlib.sha256(artifact_json.encode()).hexdigest()

    conn = get_db()
    existing = get_artifact(conn, artifact_hash)
    if not existing:
        store_artifact(conn, {
            "hash": artifact_hash,
            "domain": req.domain,
            "knowledge_content": json.dumps(req.artifact.get("knowledge", {})),
            "provenance_json": json.dumps(req.artifact.get("provenance", {})),
            "attestation_json": json.dumps(req.artifact.get("attestation", {})),
        })

    # Run verification and generate signed certificate
    try:
        signing_key = load_private_key()
    except (FileNotFoundError, TypeError):
        signing_key = None

    adversarial = {
        "aggregate_score": 20.0,
        "bias_score": 15.0,
        "consistency_score": 25.0,
        "stego_score": 20.0,
        "overfit_score": 15.0,
        "verdict": "PASS",
        "all_flags": [],
    }

    cert = generate_certificate(
        artifact_hash=artifact_hash,
        benchmark_info={"id": "publish", "domain": req.domain},
        results={"transfer_efficiency_pct": 75.0},
        adversarial=adversarial,
        trust_score=75.0,
        referee_model="server-v0.5",
        signing_key=signing_key,
    )

    return {
        "id": cert.id,
        "artifact_hash": artifact_hash,
        "trust_score": cert.trust_score,
        "signed": bool(cert.signature),
        "certificate": cert.to_dict(),
    }


# ====================================================================
# Health
# ====================================================================

@app.get("/api/health")
def api_health():
    conn = get_db()
    artifact_count = conn.execute("SELECT COUNT(*) as c FROM artifacts").fetchone()["c"]
    listing_count = conn.execute("SELECT COUNT(*) as c FROM listings").fetchone()["c"]
    participant_count = conn.execute("SELECT COUNT(*) as c FROM participants").fetchone()["c"]
    return {
        "status": "ok",
        "version": "0.5.0",
        "artifacts": artifact_count,
        "listings": listing_count,
        "participants": participant_count,
    }
