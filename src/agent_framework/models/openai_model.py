import json
import os
from typing import Any, List, Optional

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    def load_dotenv() -> None:
        return None

from ..language_model import LanguageModel
from ..message import Message
from ..model_response import ModelResponse, ToolCall
from ..tool import Tool


class OpenAIModel(LanguageModel):
    """A lightweight OpenAI adapter for framework messages and tools."""

    def __init__(self, model: str, api_key: Optional[str] = None, **kwargs: Any) -> None:
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
                "OPENAI_API_KEY is not set. Put it in your environment."
            )

        self._client = OpenAI(api_key=resolved_api_key)
        self.model = model
        self._kwargs = kwargs

    def _convert_messages(self, messages: List[Message]) -> List[dict]:
        converted = []
        for message in messages:
            payload = {"role": message.role, "content": message.content}
            if message.role == "tool":
                payload["tool_call_id"] = message.tool_call_id
            if message.tool_calls:
                payload["tool_calls"] = [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.name,
                            "arguments": json.dumps(tool_call.arguments),
                        },
                    }
                    for tool_call in message.tool_calls
                ]
            converted.append(payload)
        return converted

    def _convert_tools(self, tools: Optional[List[Tool]]) -> Optional[List[dict]]:
        if not tools:
            return None

        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                },
            }
            for tool in tools
        ]

    def _convert_response(self, response: Any) -> ModelResponse:
        message = response.choices[0].message
        content = getattr(message, "content", None)
        tool_calls = []
        for item in getattr(message, "tool_calls", []) or []:
            arguments = item.function.arguments
            if isinstance(arguments, str):
                arguments = json.loads(arguments)
            tool_calls.append(
                ToolCall(
                    id=item.id,
                    name=item.function.name,
                    arguments=arguments,
                )
            )

        return ModelResponse(content=content, tool_calls=tool_calls)

    def generate(
        self,
        messages: List[Message],
        tools: Optional[List[Tool]] = None,
    ) -> ModelResponse:
        request = {
            "model": self.model,
            "messages": self._convert_messages(messages),
            **self._kwargs,
        }

        converted_tools = self._convert_tools(tools)
        if converted_tools:
            request["tools"] = converted_tools

        response = self._client.chat.completions.create(
            **request
        )
        return self._convert_response(response)
