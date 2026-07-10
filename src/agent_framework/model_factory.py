from typing import Any

from .language_model import LanguageModel
from .models.mock_model import MockModel


def create_language_model(name: str, **kwargs: Any) -> LanguageModel:
    """Create a language model instance by provider name."""
    normalized = name.replace("-", "_").lower()

    if normalized in {"mock", "dummy"}:
        return MockModel(**kwargs)

    if normalized in {"openai", "gpt", "gpt_4", "gpt4", "gpt_3_5", "gpt3_5", "gpt-4", "gpt-3.5"}:
        from .models.openai_model import OpenAIModel

        return OpenAIModel(**kwargs)

    raise ValueError(
        f"Unknown language model '{name}'. Supported values: mock, openai."
    )
