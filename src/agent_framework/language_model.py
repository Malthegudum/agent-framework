from typing import Protocol


class LanguageModel(Protocol):
    """A provider-agnostic interface for generating text from prompts."""

    def generate(self, prompt: str) -> str:
        """Generate text for the given prompt."""
        ...
