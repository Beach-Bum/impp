#!/usr/bin/env python3
"""FastAPI server for the Agent Memory Market.

Exposes marketplace operations as HTTP endpoints.
The Carbon frontend calls these instead of using mock data.

Usage:
    uvicorn api_server:app --reload --port 8100
"""

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

app = FastAPI(title="Agent Memory Market API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
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


# --- Health ---

@app.get("/api/health")
def api_health():
    conn = get_db()
    artifact_count = conn.execute("SELECT COUNT(*) as c FROM artifacts").fetchone()["c"]
    listing_count = conn.execute("SELECT COUNT(*) as c FROM listings").fetchone()["c"]
    participant_count = conn.execute("SELECT COUNT(*) as c FROM participants").fetchone()["c"]
    return {
        "status": "ok",
        "artifacts": artifact_count,
        "listings": listing_count,
        "participants": participant_count,
    }
