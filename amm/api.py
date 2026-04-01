"""Anthropic API wrapper with retry logic and JSON parsing."""

import json
import time
import re
from anthropic import Anthropic

from .config import MODEL, API_RETRY_ATTEMPTS, API_RETRY_BASE_DELAY


def create_client() -> Anthropic:
    """Create an Anthropic API client."""
    return Anthropic()


def call_api(
    client: Anthropic,
    system: str,
    user_message: str,
    max_tokens: int = 400,
    model: str = MODEL,
) -> str:
    """Call the Anthropic API with retry logic.

    Returns the raw text response.
    """
    for attempt in range(API_RETRY_ATTEMPTS):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user_message}],
            )
            return response.content[0].text
        except Exception as e:
            if attempt < API_RETRY_ATTEMPTS - 1:
                time.sleep(API_RETRY_BASE_DELAY * (2**attempt))
                continue
            raise


def call_api_json(
    client: Anthropic,
    system: str,
    user_message: str,
    max_tokens: int = 400,
    model: str = MODEL,
    default_on_failure: dict | None = None,
) -> dict:
    """Call the API and parse the response as JSON.

    Handles markdown code blocks and common formatting issues.
    Falls back to default_on_failure if JSON parsing fails.
    """
    raw = call_api(client, system, user_message, max_tokens, model)
    return parse_json_response(raw, default_on_failure)


def parse_json_response(
    raw: str, default_on_failure: dict | None = None
) -> dict:
    """Parse a JSON response, handling markdown code blocks."""
    text = raw.strip()

    # Strip markdown code blocks
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)

    # Strip leading "json" keyword
    if text.startswith("json"):
        text = text[4:].strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        if default_on_failure is not None:
            return default_on_failure
        raise
