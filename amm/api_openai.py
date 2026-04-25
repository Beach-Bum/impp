"""OpenAI API client for cross-model transfer experiments.

Requires: pip install openai
Set OPENAI_API_KEY environment variable.
"""

import time

from .config import API_RETRY_ATTEMPTS, API_RETRY_BASE_DELAY
from .api_base import LLMClient


class OpenAIClient(LLMClient):
    """LLM client using the OpenAI API."""

    def __init__(self, model: str = "gpt-4o"):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "OpenAI SDK not installed. Run: pip install openai"
            )
        self._client = OpenAI()
        self.model = model

    def call(
        self,
        system: str,
        user_message: str,
        max_tokens: int = 400,
    ) -> str:
        for attempt in range(API_RETRY_ATTEMPTS):
            try:
                response = self._client.chat.completions.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user_message},
                    ],
                )
                return response.choices[0].message.content
            except Exception:
                if attempt < API_RETRY_ATTEMPTS - 1:
                    time.sleep(API_RETRY_BASE_DELAY * (2**attempt))
                    continue
                raise
