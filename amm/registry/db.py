"""SQLite trust registry — stores artifacts, verifications, and trust scores."""

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

from ..config import REGISTRY_DB_PATH
from ..artifact.schema import MemoryArtifact
from ..verification.certificate import VerificationCertificate


def init_db(db_path: Path | str | None = None) -> sqlite3.Connection:
    """Initialize the registry database."""
    path = str(db_path or REGISTRY_DB_PATH)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS artifacts (
            hash TEXT PRIMARY KEY,
            domain TEXT NOT NULL,
            knowledge_content TEXT NOT NULL,
            provenance_json TEXT NOT NULL,
            attestation_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            seller_id TEXT
        );

        CREATE TABLE IF NOT EXISTS benchmarks (
            id TEXT PRIMARY KEY,
            domain TEXT NOT NULL,
            config_hash TEXT NOT NULL,
            protocol_count INTEGER,
            held_out_count INTEGER,
            created_at TEXT NOT NULL,
            is_active INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS verifications (
            id TEXT PRIMARY KEY,
            artifact_hash TEXT REFERENCES artifacts(hash),
            benchmark_id TEXT REFERENCES benchmarks(id),
            certificate_json TEXT NOT NULL,
            transfer_efficiency REAL,
            adversarial_score REAL,
            trust_score REAL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS trust_scores (
            artifact_hash TEXT PRIMARY KEY REFERENCES artifacts(hash),
            current_score REAL,
            verification_count INTEGER DEFAULT 0,
            feedback_count INTEGER DEFAULT 0,
            last_updated TEXT
        );

        CREATE TABLE IF NOT EXISTS buyer_feedback (
            id TEXT PRIMARY KEY,
            artifact_hash TEXT REFERENCES artifacts(hash),
            buyer_id TEXT,
            reported_improvement REAL,
            rating INTEGER CHECK(rating BETWEEN 1 AND 5),
            feedback_text TEXT,
            created_at TEXT NOT NULL
        );

        -- Marketplace tables

        CREATE TABLE IF NOT EXISTS participants (
            id TEXT PRIMARY KEY,
            public_key_hex TEXT NOT NULL,
            display_name TEXT,
            role TEXT DEFAULT 'both',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS listings (
            id TEXT PRIMARY KEY,
            artifact_hash TEXT REFERENCES artifacts(hash),
            seller_id TEXT REFERENCES participants(id),
            title TEXT NOT NULL,
            description TEXT,
            domain TEXT NOT NULL,
            price_usd REAL NOT NULL,
            license_type TEXT DEFAULT 'licensed',
            max_buyers INTEGER DEFAULT 10,
            current_buyers INTEGER DEFAULT 0,
            status TEXT DEFAULT 'active',
            listed_at TEXT NOT NULL,
            updated_at TEXT
        );

        CREATE TABLE IF NOT EXISTS purchases (
            id TEXT PRIMARY KEY,
            listing_id TEXT REFERENCES listings(id),
            buyer_id TEXT REFERENCES participants(id),
            artifact_hash TEXT REFERENCES artifacts(hash),
            price_paid REAL NOT NULL,
            payment_method TEXT DEFAULT 'mock',
            purchased_at TEXT NOT NULL
        );

        -- Onboarding tables

        CREATE TABLE IF NOT EXISTS waitlist_entries (
            id TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            name TEXT NOT NULL,
            company TEXT DEFAULT '',
            use_case TEXT DEFAULT '',
            status TEXT DEFAULT 'pending',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS seller_applications (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            wallet TEXT DEFAULT '',
            seller_type TEXT DEFAULT '',
            description TEXT DEFAULT '',
            status TEXT DEFAULT 'pending',
            created_at TEXT NOT NULL
        );
    """)

    return conn


def store_artifact(conn: sqlite3.Connection, artifact: MemoryArtifact, seller_id: str = "") -> str:
    """Store an artifact in the registry. Returns the artifact hash."""
    conn.execute(
        """INSERT OR REPLACE INTO artifacts
           (hash, domain, knowledge_content, provenance_json, attestation_json, created_at, seller_id)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            artifact.hash,
            f"{artifact.domain.category}:{artifact.domain.subcategory}",
            artifact.knowledge.content,
            json.dumps(artifact.provenance.__dict__),
            json.dumps(artifact.attestation.__dict__),
            artifact.provenance.created_at,
            seller_id,
        ),
    )
    conn.commit()
    return artifact.hash


def store_verification(
    conn: sqlite3.Connection,
    certificate: VerificationCertificate,
) -> str:
    """Store a verification certificate. Returns the verification ID."""
    # Store benchmark if not exists
    bench = certificate.benchmark
    conn.execute(
        """INSERT OR IGNORE INTO benchmarks
           (id, domain, config_hash, protocol_count, held_out_count, created_at, is_active)
           VALUES (?, ?, ?, ?, ?, ?, 1)""",
        (
            bench["id"],
            bench["domain"],
            bench["hash"],
            bench["protocol_count"],
            bench["held_out_count"],
            datetime.now(timezone.utc).isoformat(),
        ),
    )

    # Store verification
    conn.execute(
        """INSERT INTO verifications
           (id, artifact_hash, benchmark_id, certificate_json,
            transfer_efficiency, adversarial_score, trust_score, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            certificate.id,
            certificate.artifact_hash,
            bench["id"],
            certificate.to_json(),
            certificate.results.get("transfer_efficiency_pct", 0),
            certificate.adversarial.get("aggregate_score", 0),
            certificate.trust_score,
            certificate.issued_at,
        ),
    )

    # Update trust score
    _update_trust_score(conn, certificate.artifact_hash)

    conn.commit()
    return certificate.id


def _update_trust_score(conn: sqlite3.Connection, artifact_hash: str):
    """Recompute the aggregate trust score for an artifact."""
    rows = conn.execute(
        "SELECT trust_score FROM verifications WHERE artifact_hash = ?",
        (artifact_hash,),
    ).fetchall()

    if not rows:
        return

    avg_score = sum(r["trust_score"] for r in rows) / len(rows)

    feedback_rows = conn.execute(
        "SELECT COUNT(*) as cnt FROM buyer_feedback WHERE artifact_hash = ?",
        (artifact_hash,),
    ).fetchone()

    conn.execute(
        """INSERT OR REPLACE INTO trust_scores
           (artifact_hash, current_score, verification_count, feedback_count, last_updated)
           VALUES (?, ?, ?, ?, ?)""",
        (
            artifact_hash,
            round(avg_score, 1),
            len(rows),
            feedback_rows["cnt"],
            datetime.now(timezone.utc).isoformat(),
        ),
    )


def get_trust_score(conn: sqlite3.Connection, artifact_hash: str) -> dict | None:
    """Get the current trust score for an artifact."""
    row = conn.execute(
        "SELECT * FROM trust_scores WHERE artifact_hash = ?",
        (artifact_hash,),
    ).fetchone()

    if row is None:
        return None

    return dict(row)


def get_artifact(conn: sqlite3.Connection, artifact_hash: str) -> dict | None:
    """Get an artifact by hash."""
    row = conn.execute(
        "SELECT * FROM artifacts WHERE hash = ?",
        (artifact_hash,),
    ).fetchone()

    if row is None:
        return None

    return dict(row)


def get_verifications(conn: sqlite3.Connection, artifact_hash: str) -> list[dict]:
    """Get all verifications for an artifact."""
    rows = conn.execute(
        "SELECT * FROM verifications WHERE artifact_hash = ? ORDER BY created_at DESC",
        (artifact_hash,),
    ).fetchall()

    return [dict(r) for r in rows]


def add_buyer_feedback(
    conn: sqlite3.Connection,
    artifact_hash: str,
    buyer_id: str,
    reported_improvement: float,
    rating: int,
    feedback_text: str = "",
) -> str:
    """Add buyer feedback for an artifact."""
    feedback_id = str(uuid.uuid4())
    conn.execute(
        """INSERT INTO buyer_feedback
           (id, artifact_hash, buyer_id, reported_improvement, rating, feedback_text, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            feedback_id,
            artifact_hash,
            buyer_id,
            reported_improvement,
            rating,
            feedback_text,
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    _update_trust_score(conn, artifact_hash)
    conn.commit()
    return feedback_id
