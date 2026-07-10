from typing import List, Optional, Protocol

from .message import Message
from .model_response import ModelResponse
from .tool import Tool


class LanguageModel(Protocol):
    """A provider-agnostic interface for generating responses from messages."""

    def generate(
        self,
        messages: List[Message],
        tools: Optional[List[Tool]] = None,
    ) -> ModelResponse:
        """Generate a model response for the given conversation state."""
        ...
