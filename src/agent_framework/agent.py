from dataclasses import dataclass, field
from typing import Any, List, Optional

from .tool import Tool


@dataclass
class Agent:
    """A minimal agent abstraction with optional tool access."""

    name: str
    system_instructions: str = ""
    tools: List[Tool] = field(default_factory=list)

    def run(self, input_text: Any) -> str:
        """Return a simple string description of the agent run."""
        tool_names = ", ".join(tool.name for tool in self.tools) if self.tools else "none"
        return f"Agent {self.name} ran with instructions: {self.system_instructions}. Tools: {tool_names}. Input: {input_text}"
