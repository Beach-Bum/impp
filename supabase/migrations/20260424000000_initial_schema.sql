-- Initial schema for Agent Memory Market
-- Migrated from SQLite (amm/registry/db.py)

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

CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY,
    buyer_id TEXT NOT NULL,
    listing_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL,
    confirmed_at TEXT
);
