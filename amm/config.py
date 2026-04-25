"""Configuration constants for the Agent Memory Market protocol."""

import os
from pathlib import Path

# Model
MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS_ASSESSMENT = 400
MAX_TOKENS_EXPORT = 4096
MAX_TOKENS_SCENARIO = 600

# API
API_RETRY_ATTEMPTS = 3
API_RETRY_BASE_DELAY = 1  # seconds, exponential backoff: 2^attempt

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REGISTRY_DB_PATH = DATA_DIR / "registry.db"
AMM_DIR = Path(os.environ.get("AMM_DIR", Path.home() / ".amm"))
CERTS_DIR = AMM_DIR / "certs"

# Verification
CERTIFICATE_EXPIRY_DAYS = 90
DEFAULT_TRIALS = 3

# Adversarial probe weights
ADVERSARIAL_WEIGHTS = {
    "bias": 0.30,
    "consistency": 0.25,
    "stego": 0.25,
    "overfit": 0.20,
}

# Adversarial thresholds
ADVERSARIAL_PASS_THRESHOLD = 30
ADVERSARIAL_WARN_THRESHOLD = 50

# Trust score weights
TRUST_WEIGHTS = {
    "transfer_efficiency": 0.50,
    "adversarial_clean": 0.30,  # (100 - adversarial_score)
    "freshness": 0.20,
}

# API server
API_BASE_URL = os.environ.get("AMM_API_URL", "https://api.memorymarket.ai")
JWT_SECRET = os.environ.get("AMM_JWT_SECRET", "dev-secret-change-me")
JWT_ALGORITHM = "HS256"
FREE_TIER_MONTHLY_LIMIT = 50

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
AMM_DIR.mkdir(parents=True, exist_ok=True)
CERTS_DIR.mkdir(parents=True, exist_ok=True)
