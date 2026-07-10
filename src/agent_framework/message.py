from dataclasses import dataclass, field
from typing import List, Optional, Literal

from .model_response import ToolCall

MessageRole = Literal["system", "user", "assistant", "tool"]


@dataclass
class Message:
    role: MessageRole
    content: str
    tool_call_id: Optional[str] = None
    tool_calls: List[ToolCall] = field(default_factory=list)
