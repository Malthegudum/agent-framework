from ..language_model import LanguageModel


class MockModel(LanguageModel):
    """A simple in-process model for local development and tests."""

    def __init__(self, prefix: str = "Mock response:") -> None:
        self.prefix = prefix

    def generate(self, prompt: str) -> str:
        return f"{self.prefix} {prompt}"
