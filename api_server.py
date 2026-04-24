#!/usr/bin/env python3
"""FastAPI server for the Agent Memory Market.

Exposes marketplace operations as HTTP endpoints.
Uses Supabase (Postgres) as the backing store.

Usage:
    uvicorn api_server:app --reload --port 8100

Env vars:
    SUPABASE_URL         — Supabase project URL
    SUPABASE_SERVICE_KEY — Supabase service-role key
    MARKETPLACE_API_KEY  — API key for protected endpoints
"""

import json
import os
import re
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client

from amm.marketplace.identity import create_identity
from amm.registry.trust import format_trust_report

app = FastAPI(title="Agent Memory Market API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://memorymarket.ai",
        "https://memory-market-api-production.up.railway.app",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Supabase client ---

_supabase: Client | None = None


def get_supabase() -> Client:
    global _supabase
    if _supabase is None:
        url = os.environ.get("SUPABASE_URL", "")
        key = os.environ.get("SUPABASE_SERVICE_KEY", "")
        if not url or not key:
            raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
        _supabase = create_client(url, key)
    return _supabase


# --- Auth ---

def verify_api_key(x_api_key: str = Header(...)):
    api_key = os.environ.get("MARKETPLACE_API_KEY")
    if not api_key or x_api_key != api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


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
):
    sb = get_supabase()

    # Get listings
    query = sb.table("listings").select("*").eq("status", "active")
    if domain:
        query = query.eq("domain", domain)
    if max_price is not None:
        query = query.lte("price_usd", max_price)
    listings = query.order("listed_at", desc=True).execute().data

    enriched = []
    for listing in listings:
        artifact_hash = listing["artifact_hash"]

        # Get trust score
        trust_row = sb.table("trust_scores").select("*").eq("artifact_hash", artifact_hash).maybe_single().execute().data

        # Filter by min_trust if specified
        if min_trust is not None:
            score = trust_row["current_score"] if trust_row else None
            if score is None or score < min_trust:
                continue

        # Get latest verification
        latest_v = sb.table("verifications").select("*").eq("artifact_hash", artifact_hash).order("created_at", desc=True).limit(1).execute().data
        latest_v = latest_v[0] if latest_v else None

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
            "artifact_hash": artifact_hash,
            "trust_score": trust_row["current_score"] if trust_row else None,
            "verification_count": trust_row["verification_count"] if trust_row else 0,
            "feedback_count": trust_row["feedback_count"] if trust_row else 0,
            "latest_transfer_efficiency": latest_v["transfer_efficiency"] if latest_v else None,
            "latest_adversarial_score": latest_v["adversarial_score"] if latest_v else None,
        })

    return {"listings": enriched}


@app.get("/api/listings/{listing_id}")
def api_get_listing(listing_id: str):
    sb = get_supabase()
    row = sb.table("listings").select("*").eq("id", listing_id).maybe_single().execute().data
    if not row:
        raise HTTPException(status_code=404, detail="Listing not found")
    return row


# --- Artifacts ---

@app.get("/api/artifacts/{artifact_hash}")
def api_get_artifact(artifact_hash: str):
    sb = get_supabase()
    row = sb.table("artifacts").select("*").eq("hash", artifact_hash).maybe_single().execute().data
    if not row:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return row


@app.get("/api/artifacts/{artifact_hash}/preview")
def api_get_preview(artifact_hash: str):
    sb = get_supabase()
    artifact_data = sb.table("artifacts").select("*").eq("hash", artifact_hash).maybe_single().execute().data
    if not artifact_data:
        raise HTTPException(status_code=404, detail="Artifact not found")

    trust = sb.table("trust_scores").select("*").eq("artifact_hash", artifact_hash).maybe_single().execute().data
    verifications = sb.table("verifications").select("*").eq("artifact_hash", artifact_hash).order("created_at", desc=True).execute().data
    latest_v = verifications[0] if verifications else None

    from amm.marketplace.preview import generate_preview
    from amm.artifact.schema import MemoryArtifact

    artifact = MemoryArtifact.from_dict({
        "domain": {"category": artifact_data["domain"].split(":")[0], "subcategory": artifact_data["domain"].split(":")[-1]},
        "knowledge": {"format": "markdown", "content": artifact_data["knowledge_content"], "sections": [], "token_count": len(artifact_data["knowledge_content"].split())},
        "provenance": json.loads(artifact_data["provenance_json"]) if isinstance(artifact_data["provenance_json"], str) else artifact_data["provenance_json"],
        "attestation": json.loads(artifact_data["attestation_json"]) if isinstance(artifact_data["attestation_json"], str) else artifact_data["attestation_json"],
        "hash": artifact_data["hash"],
    })

    preview = generate_preview(artifact, trust, latest_v)
    return preview


# --- Trust ---

@app.get("/api/trust/{artifact_hash}")
def api_get_trust(artifact_hash: str):
    sb = get_supabase()
    trust = sb.table("trust_scores").select("*").eq("artifact_hash", artifact_hash).maybe_single().execute().data
    if not trust:
        raise HTTPException(status_code=404, detail="No trust data")
    verifications = sb.table("verifications").select("*").eq("artifact_hash", artifact_hash).order("created_at", desc=True).execute().data
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
    sb = get_supabase()
    feedback_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    sb.table("buyer_feedback").insert({
        "id": feedback_id,
        "artifact_hash": artifact_hash,
        "buyer_id": req.buyer_id,
        "reported_improvement": req.improvement,
        "rating": req.rating,
        "feedback_text": req.text,
        "created_at": now,
    }).execute()

    # Recompute trust score
    _update_trust_score(sb, artifact_hash)

    trust = sb.table("trust_scores").select("*").eq("artifact_hash", artifact_hash).maybe_single().execute().data
    return {"feedback_id": feedback_id, "updated_trust": trust}


def _update_trust_score(sb: Client, artifact_hash: str):
    """Recompute aggregate trust score for an artifact."""
    rows = sb.table("verifications").select("trust_score").eq("artifact_hash", artifact_hash).execute().data
    if not rows:
        return

    avg_score = sum(r["trust_score"] for r in rows) / len(rows)

    feedback_rows = sb.table("buyer_feedback").select("id", count="exact").eq("artifact_hash", artifact_hash).execute()
    feedback_count = feedback_rows.count if feedback_rows.count is not None else 0

    now = datetime.now(timezone.utc).isoformat()
    sb.table("trust_scores").upsert({
        "artifact_hash": artifact_hash,
        "current_score": round(avg_score, 1),
        "verification_count": len(rows),
        "feedback_count": feedback_count,
        "last_updated": now,
    }).execute()


# --- Identity ---

class IdentityRequest(BaseModel):
    display_name: str

@app.post("/api/identity")
def api_create_identity(req: IdentityRequest):
    sb = get_supabase()
    identity = create_identity(req.display_name)
    sb.table("participants").upsert({
        "id": identity["id"],
        "public_key_hex": identity["public_key_hex"],
        "display_name": identity["display_name"],
        "role": "both",
        "created_at": identity["created_at"],
    }).execute()
    return {
        "id": identity["id"],
        "display_name": identity["display_name"],
        "public_key_hex": identity["public_key_hex"],
    }

@app.get("/api/identity/{participant_id}")
def api_get_identity(participant_id: str):
    sb = get_supabase()
    row = sb.table("participants").select("*").eq("id", participant_id).maybe_single().execute().data
    if not row:
        raise HTTPException(status_code=404, detail="Participant not found")
    return row


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
    sb = get_supabase()

    # Validate artifact exists
    artifact = sb.table("artifacts").select("hash, domain").eq("hash", req.artifact_hash).maybe_single().execute().data
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")

    # Validate seller exists
    seller = sb.table("participants").select("id").eq("id", req.seller_id).maybe_single().execute().data
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    if req.price_usd < 0.01 or req.price_usd > 10000:
        raise HTTPException(status_code=400, detail="Price must be between $0.01 and $10,000")

    listing_id = str(uuid.uuid4())[:8]
    now = datetime.now(timezone.utc).isoformat()

    max_buyers = 1 if req.license_type == "exclusive" else req.max_buyers

    sb.table("listings").insert({
        "id": listing_id,
        "artifact_hash": req.artifact_hash,
        "seller_id": req.seller_id,
        "title": req.title,
        "description": req.description,
        "domain": artifact["domain"],
        "price_usd": req.price_usd,
        "license_type": req.license_type,
        "max_buyers": max_buyers,
        "current_buyers": 0,
        "status": "active",
        "listed_at": now,
        "updated_at": now,
    }).execute()

    return {"listing_id": listing_id}


# --- Portfolio / Control Tower ---

@app.get("/api/portfolio")
def api_portfolio():
    sb = get_supabase()

    # Stats
    listing_res = sb.table("listings").select("id", count="exact").eq("status", "active").execute()
    listing_count = listing_res.count or 0

    verification_res = sb.table("verifications").select("id", count="exact").execute()
    verification_count = verification_res.count or 0

    feedback_res = sb.table("buyer_feedback").select("id", count="exact").execute()
    feedback_count = feedback_res.count or 0

    # Recent verifications — need to join manually since supabase-py doesn't do complex joins
    recent_verifications = sb.table("verifications").select("*").order("created_at", desc=True).limit(10).execute().data

    agents = []
    for v in recent_verifications:
        artifact_hash = v["artifact_hash"]

        # Get artifact domain
        art = sb.table("artifacts").select("domain").eq("hash", artifact_hash).maybe_single().execute().data
        domain = art["domain"] if art else "unknown"

        # Get listing title
        listing = sb.table("listings").select("title").eq("artifact_hash", artifact_hash).maybe_single().execute().data
        title = listing["title"] if listing else artifact_hash[:12]

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
            "name": title,
            "memory": domain,
            "status": status,
            "trust_score": v["trust_score"],
            "transfer_efficiency": te,
            "adversarial_score": adv,
            "last_eval": v["created_at"],
        })

    # Alerts
    alert_rows = sb.table("verifications").select("artifact_hash, adversarial_score, transfer_efficiency").or_("adversarial_score.gt.25,transfer_efficiency.lt.0").execute().data

    alerts = []
    for r in alert_rows:
        artifact_hash = r["artifact_hash"]
        listing = sb.table("listings").select("title").eq("artifact_hash", artifact_hash).maybe_single().execute().data
        title = listing["title"] if listing else artifact_hash[:12]

        if (r["transfer_efficiency"] or 0) < 0:
            alerts.append({
                "id": artifact_hash[:8],
                "title": f"Negative transfer on {title}",
                "severity": "Blocked",
                "summary": f"Transfer efficiency is {r['transfer_efficiency']:.1f}%. Artifact should be revoked.",
            })
        elif (r["adversarial_score"] or 0) > 40:
            alerts.append({
                "id": artifact_hash[:8],
                "title": f"High adversarial score on {title}",
                "severity": "Warning",
                "summary": f"Adversarial score {r['adversarial_score']:.1f}/100 exceeds warning threshold.",
            })

    # Total spend
    active_listings = sb.table("listings").select("price_usd").eq("status", "active").execute().data
    total_spend = sum(l["price_usd"] for l in active_listings) if active_listings else 0

    return {
        "stats": {
            "active_listings": listing_count,
            "verifications": verification_count,
            "feedback_received": feedback_count,
            "monthly_spend": total_spend,
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
def api_waitlist(req: WaitlistRequest):
    if not _EMAIL_RE.match(req.email):
        raise HTTPException(status_code=422, detail="Invalid email address")
    sb = get_supabase()
    entry_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    sb.table("waitlist_entries").insert({
        "id": entry_id,
        "email": req.email,
        "name": req.name,
        "company": req.company,
        "use_case": req.use_case,
        "status": "pending",
        "created_at": now,
    }).execute()
    return {"id": entry_id, "status": "pending"}


# --- Seller Apply ---

class SellerApplyRequest(BaseModel):
    name: str
    email: str
    wallet: str = ""
    seller_type: str = ""
    description: str = ""

@app.post("/api/seller-apply")
def api_seller_apply(req: SellerApplyRequest):
    if not _EMAIL_RE.match(req.email):
        raise HTTPException(status_code=422, detail="Invalid email address")
    sb = get_supabase()
    app_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    sb.table("seller_applications").insert({
        "id": app_id,
        "name": req.name,
        "email": req.email,
        "wallet": req.wallet,
        "seller_type": req.seller_type,
        "description": req.description,
        "status": "pending",
        "created_at": now,
    }).execute()
    return {"id": app_id, "status": "pending"}


# --- Orders ---

class OrderRequest(BaseModel):
    buyer_id: str
    listing_id: str

@app.post("/api/orders")
def api_create_order(req: OrderRequest):
    sb = get_supabase()
    listing = sb.table("listings").select("*").eq("id", req.listing_id).maybe_single().execute().data
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if listing["status"] != "active":
        raise HTTPException(status_code=400, detail="Listing is not active")
    order_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    sb.table("orders").insert({
        "id": order_id,
        "buyer_id": req.buyer_id,
        "listing_id": req.listing_id,
        "status": "pending",
        "created_at": now,
    }).execute()
    return {"id": order_id, "buyer_id": req.buyer_id, "listing_id": req.listing_id, "status": "pending", "created_at": now}


@app.get("/api/orders/{order_id}")
def api_get_order(order_id: str):
    sb = get_supabase()
    row = sb.table("orders").select("*").eq("id", order_id).maybe_single().execute().data
    if not row:
        raise HTTPException(status_code=404, detail="Order not found")
    return row


@app.post("/api/orders/{order_id}/confirm")
def api_confirm_order(order_id: str):
    sb = get_supabase()
    now = datetime.now(timezone.utc).isoformat()

    # Check current state
    row = sb.table("orders").select("*").eq("id", order_id).maybe_single().execute().data
    if not row:
        raise HTTPException(status_code=404, detail="Order not found")
    if row["status"] != "pending":
        raise HTTPException(status_code=400, detail="Order is not in pending status")

    # Update
    sb.table("orders").update({"status": "confirmed", "confirmed_at": now}).eq("id", order_id).eq("status", "pending").execute()

    updated = sb.table("orders").select("*").eq("id", order_id).maybe_single().execute().data
    return updated


# --- Health ---

@app.get("/api/health")
def api_health():
    sb = get_supabase()
    artifact_count = sb.table("artifacts").select("hash", count="exact").execute().count or 0
    listing_count = sb.table("listings").select("id", count="exact").execute().count or 0
    participant_count = sb.table("participants").select("id", count="exact").execute().count or 0
    return {
        "status": "ok",
        "artifacts": artifact_count,
        "listings": listing_count,
        "participants": participant_count,
    }
