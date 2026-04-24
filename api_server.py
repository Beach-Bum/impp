#!/usr/bin/env python3
"""FastAPI server for the Agent Memory Market.

Exposes marketplace operations as HTTP endpoints.
The Carbon frontend calls these instead of using mock data.

Usage:
    uvicorn api_server:app --reload --port 8100
"""

import os
import re
import sqlite3
import uuid
from typing import Generator

from fastapi import FastAPI, HTTPException, Header, Depends
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
    allow_origins=["http://localhost:3000", "https://memorymarket.ai"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Auth ---

def verify_api_key(x_api_key: str = Header(...)):
    api_key = os.environ.get("MARKETPLACE_API_KEY")
    if not api_key or x_api_key != api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


# --- DB ---

def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = init_db()
    try:
        yield conn
    finally:
        conn.close()


# --- Health ---

@app.get("/health")
def health():
    return {"status": "ok"}


# --- Listings ---

@app.get("/api/listings")
def api_search_listings(
    domain: str | None = None,
    min_trust: float | None = None,
    max_price: float | None = None,
    conn: sqlite3.Connection = Depends(get_db),
):
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
def api_get_listing(listing_id: str, conn: sqlite3.Connection = Depends(get_db)):
    listing = get_listing(conn, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing


# --- Artifacts ---

@app.get("/api/artifacts/{artifact_hash}")
def api_get_artifact(artifact_hash: str, conn: sqlite3.Connection = Depends(get_db)):
    artifact = get_artifact(conn, artifact_hash)
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return artifact


@app.get("/api/artifacts/{artifact_hash}/preview")
def api_get_preview(artifact_hash: str, conn: sqlite3.Connection = Depends(get_db)):
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
def api_get_trust(artifact_hash: str, conn: sqlite3.Connection = Depends(get_db)):
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
def api_add_feedback(artifact_hash: str, req: FeedbackRequest, conn: sqlite3.Connection = Depends(get_db)):
    feedback_id = add_buyer_feedback(
        conn, artifact_hash, req.buyer_id, req.improvement, req.rating, req.text,
    )
    trust = get_trust_score(conn, artifact_hash)
    return {"feedback_id": feedback_id, "updated_trust": trust}


# --- Identity ---

class IdentityRequest(BaseModel):
    display_name: str

@app.post("/api/identity")
def api_create_identity(req: IdentityRequest, conn: sqlite3.Connection = Depends(get_db)):
    identity = create_identity(req.display_name)
    register_participant(conn, identity)
    return {
        "id": identity["id"],
        "display_name": identity["display_name"],
        "public_key_hex": identity["public_key_hex"],
    }

@app.get("/api/identity/{participant_id}")
def api_get_identity(participant_id: str, conn: sqlite3.Connection = Depends(get_db)):
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
def api_create_listing(req: ListingRequest, conn: sqlite3.Connection = Depends(get_db)):
    listing_id = create_listing(
        conn, req.artifact_hash, req.seller_id, req.title,
        req.description, req.price_usd, req.license_type, req.max_buyers,
    )
    return {"listing_id": listing_id}


# --- Portfolio / Control Tower ---

@app.get("/api/portfolio")
def api_portfolio(conn: sqlite3.Connection = Depends(get_db)):
    """Get control tower data: active listings, recent verifications, alerts."""

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


# --- Waitlist ---

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

class WaitlistRequest(BaseModel):
    email: str
    name: str
    company: str = ""
    use_case: str = ""

@app.post("/api/waitlist")
def api_waitlist(req: WaitlistRequest, conn: sqlite3.Connection = Depends(get_db)):
    if not _EMAIL_RE.match(req.email):
        raise HTTPException(status_code=422, detail="Invalid email address")
    entry_id = str(uuid.uuid4())
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """INSERT INTO waitlist_entries (id, email, name, company, use_case, status, created_at)
           VALUES (?, ?, ?, ?, ?, 'pending', ?)""",
        (entry_id, req.email, req.name, req.company, req.use_case, now),
    )
    conn.commit()
    return {"id": entry_id, "status": "pending"}


# --- Seller Apply ---

class SellerApplyRequest(BaseModel):
    name: str
    email: str
    wallet: str = ""
    seller_type: str = ""
    description: str = ""

@app.post("/api/seller-apply")
def api_seller_apply(req: SellerApplyRequest, conn: sqlite3.Connection = Depends(get_db)):
    if not _EMAIL_RE.match(req.email):
        raise HTTPException(status_code=422, detail="Invalid email address")
    app_id = str(uuid.uuid4())
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """INSERT INTO seller_applications (id, name, email, wallet, seller_type, description, status, created_at)
           VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)""",
        (app_id, req.name, req.email, req.wallet, req.seller_type, req.description, now),
    )
    conn.commit()
    return {"id": app_id, "status": "pending"}


# --- Orders ---

class OrderRequest(BaseModel):
    buyer_id: str
    listing_id: str

@app.post("/api/orders", dependencies=[Depends(verify_api_key)])
def api_create_order(req: OrderRequest, conn: sqlite3.Connection = Depends(get_db)):
    listing = get_listing(conn, req.listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if listing["status"] != "active":
        raise HTTPException(status_code=400, detail="Listing is not active")
    from datetime import datetime, timezone
    order_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """INSERT INTO orders (id, buyer_id, listing_id, status, created_at)
           VALUES (?, ?, ?, 'pending', ?)""",
        (order_id, req.buyer_id, req.listing_id, now),
    )
    conn.commit()
    return {"id": order_id, "buyer_id": req.buyer_id, "listing_id": req.listing_id, "status": "pending", "created_at": now}


@app.get("/api/orders/{order_id}")
def api_get_order(order_id: str, conn: sqlite3.Connection = Depends(get_db)):
    row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Order not found")
    return dict(row)


@app.post("/api/orders/{order_id}/confirm", dependencies=[Depends(verify_api_key)])
def api_confirm_order(order_id: str, conn: sqlite3.Connection = Depends(get_db)):
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat()
    # Atomic check-and-update to prevent double-confirmation races
    cursor = conn.execute(
        "UPDATE orders SET status = 'confirmed', confirmed_at = ? WHERE id = ? AND status = 'pending'",
        (now, order_id),
    )
    conn.commit()
    if cursor.rowcount == 0:
        row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Order not found")
        raise HTTPException(status_code=400, detail="Order is not in pending status")
    updated = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    return dict(updated)


# --- Health ---

@app.get("/api/health")
def api_health(conn: sqlite3.Connection = Depends(get_db)):
    artifact_count = conn.execute("SELECT COUNT(*) as c FROM artifacts").fetchone()["c"]
    listing_count = conn.execute("SELECT COUNT(*) as c FROM listings").fetchone()["c"]
    participant_count = conn.execute("SELECT COUNT(*) as c FROM participants").fetchone()["c"]
    return {
        "status": "ok",
        "artifacts": artifact_count,
        "listings": listing_count,
        "participants": participant_count,
    }
