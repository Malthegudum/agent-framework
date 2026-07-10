from dataclasses import dataclass, field
from typing import Any, List, Optional

from .language_model import LanguageModel
from .message import Message
from .tool import Tool


@dataclass
class Agent:
    """A minimal agent abstraction with optional tool access and model support."""

    name: str
    system_instructions: str = ""
    tools: List[Tool] = field(default_factory=list)
    model: Optional[LanguageModel] = None
    max_iterations: int = 10

    @classmethod
    def with_model(
        cls,
        name: str,
        model_name: str,
        system_instructions: str = "",
        tools: Optional[List[Tool]] = None,
        **model_kwargs: Any,
    ) -> "Agent":
        """Create an agent configured with a named language model."""
        from .model_factory import create_language_model

        model = create_language_model(model_name, **model_kwargs)
        return cls(name=name, system_instructions=system_instructions, tools=tools or [], model=model)

    def _get_tool(self, name: str) -> Tool:
        for tool in self.tools:
            if tool.name == name:
                return tool

        raise ValueError(f"Agent '{self.name}' does not have a tool named '{name}'.")

    def run(self, input_text: Any) -> str:
        """Run the model/tool loop until the model returns final text."""
        if self.model is None:
            raise RuntimeError(f"Agent '{self.name}' cannot run without a model.")

        messages: List[Message] = []
        if self.system_instructions:
            messages.append(Message(role="system", content=self.system_instructions))
        messages.append(Message(role="user", content=str(input_text)))

        for _ in range(self.max_iterations):
            response = self.model.generate(messages=messages, tools=self.tools)

            if not response.tool_calls:
                return response.content or ""

            messages.append(
                Message(
                    role="assistant",
                    content=response.content or "",
                    tool_calls=response.tool_calls,
                )
            )

            for tool_call in response.tool_calls:
                tool = self._get_tool(tool_call.name)
                result = tool.execute(**tool_call.arguments)
                messages.append(
                    Message(
                        role="tool",
                        content=str(result),
                        tool_call_id=tool_call.id,
                    )
                )

        raise RuntimeError(
            f"Agent '{self.name}' exceeded the maximum iterations of {self.max_iterations}."
        )
