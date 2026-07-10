import os
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv

from ..language_model import LanguageModel


class OpenAIModel(LanguageModel):
    """A lightweight OpenAI adapter that implements the LanguageModel protocol."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4", **kwargs: Any) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "openai package is required for OpenAIModel. "
                "Install it with `pip install openai`."
            ) from exc

        load_dotenv()
        resolved_api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not resolved_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Put it in your environment or in a .env file."
            )

        self._client = OpenAI(api_key=resolved_api_key)
        self.model = model
        self._kwargs = kwargs

    def generate(self, prompt: str) -> str:
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            **self._kwargs,
        )
        return response.choices[0].message.content.strip()
