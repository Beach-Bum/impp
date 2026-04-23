"""Ollama API client for local model transfer experiments.

Uses Ollama's OpenAI-compatible API endpoint. No extra dependencies needed.
Requires Ollama running locally: https://ollama.com
"""

import json
import time
import urllib.request
import urllib.error

from .config import API_RETRY_ATTEMPTS, API_RETRY_BASE_DELAY
from .api_base import LLMClient


class OllamaClient(LLMClient):
    """LLM client using Ollama's OpenAI-compatible API."""

    def __init__(self, model: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url.rstrip("/")

    def call(
        self,
        system: str,
        user_message: str,
        max_tokens: int = 400,
    ) -> str:
        url = f"{self.base_url}/v1/chat/completions"
        payload = json.dumps({
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user_message},
            ],
        }).encode("utf-8")

        headers = {"Content-Type": "application/json"}

        for attempt in range(API_RETRY_ATTEMPTS):
            try:
                req = urllib.request.Request(url, data=payload, headers=headers)
                with urllib.request.urlopen(req, timeout=120) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]
            except (urllib.error.URLError, urllib.error.HTTPError, KeyError):
                if attempt < API_RETRY_ATTEMPTS - 1:
                    time.sleep(API_RETRY_BASE_DELAY * (2**attempt))
                    continue
                raise
