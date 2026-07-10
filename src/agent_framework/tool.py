from dataclasses import dataclass
from typing import Any, Callable, Dict


@dataclass
class Tool:
    """A simple wrapper around a Python callable with an explicit schema."""

    name: str
    description: str
    func: Callable[..., Any]
    parameters: Dict[str, Any]

    def execute(self, **arguments: Any) -> Any:
        """Call the wrapped Python function with the provided keyword arguments."""
        return self.func(**arguments)
