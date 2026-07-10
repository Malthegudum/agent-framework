from dataclasses import dataclass
from typing import Any, Callable, Optional


@dataclass
class Tool:
    """A simple wrapper around a Python callable."""

    name: str
    description: str
    func: Callable[..., Any]

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Call the wrapped Python function with the provided arguments."""
        return self.func(*args, **kwargs)
