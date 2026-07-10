from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: Dict[str, Any]


@dataclass
class ModelResponse:
    content: Optional[str] = None
    tool_calls: List[ToolCall] = field(default_factory=list)
