"""Anthropic API wrapper with retry logic and JSON parsing.

Also provides the factory function for creating clients based on provider.
"""

import time
from anthropic import Anthropic

from .config import MODEL, API_RETRY_ATTEMPTS, API_RETRY_BASE_DELAY
from .api_base import LLMClient, parse_json_response


class AnthropicClient(LLMClient):
    """LLM client using the Anthropic API."""

    def __init__(self, model: str = MODEL):
        self._client = Anthropic()
        self.model = model

    def call(
        self,
        system: str,
        user_message: str,
        max_tokens: int = 400,
    ) -> str:
        for attempt in range(API_RETRY_ATTEMPTS):
            try:
                response = self._client.messages.create(
                    model=self.model,
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


# --- Backwards-compatible API ---
# These functions maintain compatibility with all existing call sites.


def create_client() -> Anthropic:
    """Create a raw Anthropic client (legacy compatibility)."""
    return Anthropic()


def create_llm_client(provider: str = "anthropic", model: str = "", **kwargs) -> LLMClient:
    """Create an LLMClient for the given provider.

    Args:
        provider: 'anthropic', 'openai', or 'ollama'
        model: Model name override
        **kwargs: Provider-specific options (e.g., ollama_base_url)

    Returns:
        An LLMClient instance.
    """
    if provider == "anthropic":
        return AnthropicClient(model=model or MODEL)
    elif provider == "openai":
        from .api_openai import OpenAIClient
        return OpenAIClient(model=model or "gpt-4o")
    elif provider == "ollama":
        from .api_ollama import OllamaClient
        return OllamaClient(
            model=model or "llama3",
            base_url=kwargs.get("ollama_base_url", "http://localhost:11434"),
        )
    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'anthropic', 'openai', or 'ollama'.")


def call_api(
    client: Anthropic,
    system: str,
    user_message: str,
    max_tokens: int = 400,
    model: str = MODEL,
) -> str:
    """Call the Anthropic API with retry logic (legacy compatibility).

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
    """Call the API and parse the response as JSON (legacy compatibility)."""
    raw = call_api(client, system, user_message, max_tokens, model)
    return parse_json_response(raw, default_on_failure)
