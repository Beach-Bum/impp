"""Test configuration.

amm.config refuses to import without AMM_JWT_SECRET unless AMM_TESTING=1.
Setting it here lets `python -m pytest tests` collect without any
environment set up by hand. No test needs a real secret or the network.
"""

import os

os.environ.setdefault("AMM_TESTING", "1")
