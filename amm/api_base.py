"""Abstract base for LLM client implementations.

All LLM interactions go through this protocol, making the system
model-agnostic. Swap Anthropic for OpenAI or Ollama by changing the client.
"""

import json
import re
from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Protocol for LLM API clients."""

    @abstractmethod
    def call(
        self,
        system: str,
        user_message: str,
        max_tokens: int = 400,
    ) -> str:
        """Call the LLM and return raw text response."""
        ...

    def call_json(
        self,
        system: str,
        user_message: str,
        max_tokens: int = 400,
        default_on_failure: dict | None = None,
    ) -> dict:
        """Call the LLM and parse response as JSON."""
        raw = self.call(system, user_message, max_tokens)
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
