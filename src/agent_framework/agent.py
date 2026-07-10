from dataclasses import dataclass, field
from typing import Any, List, Optional

from .language_model import LanguageModel
from .tool import Tool


@dataclass
class Agent:
    """A minimal agent abstraction with optional tool access and model support."""

    name: str
    system_instructions: str = ""
    tools: List[Tool] = field(default_factory=list)
    model: Optional[LanguageModel] = None

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

    def _build_prompt(self, input_text: Any) -> str:
        tool_info = "\n".join(f"{tool.name}: {tool.description}" for tool in self.tools)
        tools_section = f"\nTools:\n{tool_info}\n" if tool_info else ""
        return (
            f"System: {self.system_instructions}\n"
            f"{tools_section}"
            f"User: {input_text}"
        )

    def run(self, input_text: Any) -> str:
        """Return the agent response, using a model if available."""
        if self.model is None:
            tool_names = ", ".join(tool.name for tool in self.tools) if self.tools else "none"
            return (
                f"Agent {self.name} ran with instructions: {self.system_instructions}. "
                f"Tools: {tool_names}. Input: {input_text}"
            )

        prompt = self._build_prompt(input_text)
        return self.model.generate(prompt)
