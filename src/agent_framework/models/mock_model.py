from typing import List, Optional

from ..language_model import LanguageModel
from ..message import Message
from ..model_response import ModelResponse
from ..tool import Tool


class MockModel(LanguageModel):
    """A simple in-process model for local development and tests."""

    def __init__(self, prefix: str = "Mock response:") -> None:
        self.prefix = prefix

    def generate(
        self,
        messages: List[Message],
        tools: Optional[List[Tool]] = None,
    ) -> ModelResponse:
        return ModelResponse(content=self.prefix)
