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

# Adversarial risk thresholds (lower = cleaner artifact)
# Risk score 0-100: composite of bias, consistency, stego, overfit probes.
# 0-30 = PASS (clean), 31-50 = WARNING (review recommended), 51-100 = FAIL (reject).
ADVERSARIAL_RISK_PASS_CEILING = 30   # at or below: artifact passes
ADVERSARIAL_RISK_WARN_CEILING = 50   # at or below: warning; above: fail

# Trust score weights
TRUST_WEIGHTS = {
    "transfer_efficiency": 0.50,
    "adversarial_clean": 0.30,  # (100 - adversarial_risk); higher = cleaner
    "freshness": 0.20,
}

# API server
API_BASE_URL = os.environ.get("AMM_API_URL", "https://api.memorymarket.ai")
JWT_SECRET = os.environ.get("AMM_JWT_SECRET")
if not JWT_SECRET and os.environ.get("AMM_TESTING") != "1":
    raise RuntimeError("AMM_JWT_SECRET environment variable must be set")
JWT_ALGORITHM = "HS256"
FREE_TIER_MONTHLY_LIMIT = 50

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
AMM_DIR.mkdir(parents=True, exist_ok=True)
CERTS_DIR.mkdir(parents=True, exist_ok=True)
