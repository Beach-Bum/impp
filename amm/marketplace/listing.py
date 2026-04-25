"""Artifact listing and search for the memory marketplace."""

import uuid
from datetime import datetime, timezone


def create_listing(
    conn,
    artifact_hash: str,
    seller_id: str,
    title: str,
    description: str,
    price_usd: float,
    license_type: str = "licensed",
    max_buyers: int = 10,
) -> str:
    """Create a new marketplace listing for an artifact.

    Args:
        conn: Database connection
        artifact_hash: Hash of the artifact to list
        seller_id: Seller's participant ID
        title: Listing title
        description: Listing description
        price_usd: Price in USD
        license_type: 'exclusive', 'licensed', or 'subscription'
        max_buyers: Maximum number of buyers (for licensed model)

    Returns:
        Listing ID.

    Raises:
        ValueError: If artifact doesn't exist, seller not found, or invalid params.
    """
    # Validate artifact exists
    artifact = conn.execute(
        "SELECT hash, domain FROM artifacts WHERE hash = ?",
        (artifact_hash,),
    ).fetchone()
    if not artifact:
        raise ValueError(f"Artifact not found: {artifact_hash}")

    # Validate seller exists
    seller = conn.execute(
        "SELECT id FROM participants WHERE id = ?",
        (seller_id,),
    ).fetchone()
    if not seller:
        raise ValueError(f"Seller not found: {seller_id}")

    if price_usd < 0.01 or price_usd > 10000:
        raise ValueError(f"Price must be between $0.01 and $10,000 (got ${price_usd})")

    if license_type not in ("exclusive", "licensed", "subscription"):
        raise ValueError(f"Invalid license type: {license_type}")

    if license_type == "exclusive":
        max_buyers = 1

    listing_id = str(uuid.uuid4())[:8]
    now = datetime.now(timezone.utc).isoformat()

    conn.execute(
        """INSERT INTO listings
           (id, artifact_hash, seller_id, title, description, domain,
            price_usd, license_type, max_buyers, current_buyers, status, listed_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 'active', ?, ?)""",
        (
            listing_id,
            artifact_hash,
            seller_id,
            title,
            description,
            artifact["domain"],
            price_usd,
            license_type,
            max_buyers,
            now,
            now,
        ),
    )
    conn.commit()
    return listing_id


def search_listings(
    conn,
    domain: str | None = None,
    min_trust: float | None = None,
    max_price: float | None = None,
    status: str = "active",
) -> list[dict]:
    """Search available artifact listings.

    Args:
        conn: Database connection
        domain: Filter by domain (e.g., 'DeFi:risk-assessment')
        min_trust: Minimum trust score
        max_price: Maximum price in USD
        status: Listing status filter (default: 'active')

    Returns:
        List of listing dicts with trust score joined.
    """
    query = """
        SELECT l.*, t.current_score as trust_score
        FROM listings l
        LEFT JOIN trust_scores t ON l.artifact_hash = t.artifact_hash
        WHERE l.status = ?
    """
    params: list = [status]

    if domain:
        query += " AND l.domain = ?"
        params.append(domain)

    if min_trust is not None:
        query += " AND (t.current_score >= ? OR t.current_score IS NULL)"
        params.append(min_trust)

    if max_price is not None:
        query += " AND l.price_usd <= ?"
        params.append(max_price)

    query += " ORDER BY t.current_score DESC NULLS LAST, l.listed_at DESC"

    rows = conn.execute(query, params).fetchall()
    return [dict(r) for r in rows]


def get_listing(conn, listing_id: str) -> dict | None:
    """Get a single listing by ID with trust score."""
    row = conn.execute(
        """SELECT l.*, t.current_score as trust_score
           FROM listings l
           LEFT JOIN trust_scores t ON l.artifact_hash = t.artifact_hash
           WHERE l.id = ?""",
        (listing_id,),
    ).fetchone()
    return dict(row) if row else None


def delist(conn, listing_id: str, seller_id: str) -> bool:
    """Mark a listing as delisted. Only the seller can delist.

    Returns True if delisted, False if not found or not authorized.
    """
    result = conn.execute(
        """UPDATE listings SET status = 'delisted', updated_at = ?
           WHERE id = ? AND seller_id = ? AND status = 'active'""",
        (datetime.now(timezone.utc).isoformat(), listing_id, seller_id),
    )
    conn.commit()
    return result.rowcount > 0
