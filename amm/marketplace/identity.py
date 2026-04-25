"""Participant identity for the memory marketplace.

Simple keypair-based identity. No external auth server needed.
The secret key file IS the authentication.
"""

import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_IDENTITY_PATH = Path.home() / ".amm" / "identity.json"


def create_identity(display_name: str) -> dict:
    """Create a new marketplace participant identity.

    Returns:
        {
            "id": participant ID (hex hash of public key),
            "display_name": display name,
            "public_key_hex": hex-encoded public key,
            "secret_key_hex": hex-encoded secret key (keep private!),
            "created_at": ISO 8601 timestamp,
        }
    """
    secret_key = os.urandom(32)
    public_key = hashlib.sha256(secret_key).digest()
    participant_id = hashlib.sha256(public_key).hexdigest()[:16]

    return {
        "id": participant_id,
        "display_name": display_name,
        "public_key_hex": public_key.hex(),
        "secret_key_hex": secret_key.hex(),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def save_identity(identity: dict, path: Path | str | None = None):
    """Save identity to disk."""
    path = Path(path or DEFAULT_IDENTITY_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(identity, f, indent=2)


def load_identity(path: Path | str | None = None) -> dict | None:
    """Load identity from disk. Returns None if not found."""
    path = Path(path or DEFAULT_IDENTITY_PATH)
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def register_participant(conn, identity: dict, role: str = "both"):
    """Register a participant in the registry database."""
    conn.execute(
        """INSERT OR REPLACE INTO participants
           (id, public_key_hex, display_name, role, created_at)
           VALUES (?, ?, ?, ?, ?)""",
        (
            identity["id"],
            identity["public_key_hex"],
            identity["display_name"],
            role,
            identity["created_at"],
        ),
    )
    conn.commit()


def get_participant(conn, participant_id: str) -> dict | None:
    """Look up a participant by ID."""
    row = conn.execute(
        "SELECT * FROM participants WHERE id = ?",
        (participant_id,),
    ).fetchone()
    return dict(row) if row else None


def verify_ownership(identity: dict, participant_id: str) -> bool:
    """Verify that an identity corresponds to a participant ID."""
    public_key = hashlib.sha256(
        bytes.fromhex(identity["secret_key_hex"])
    ).digest()
    derived_id = hashlib.sha256(public_key).hexdigest()[:16]
    return derived_id == participant_id
