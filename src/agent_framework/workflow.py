from dataclasses import dataclass, field
from typing import Any, Callable, List


Step = Callable[[Any], Any]


@dataclass
class Workflow:
    """A minimal ordered workflow that executes steps sequentially."""

    steps: List[Step] = field(default_factory=list)

    def add_step(self, step: Step) -> None:
        """Append a step to the workflow."""
        self.steps.append(step)

    def run(self, initial_value: Any) -> Any:
        """Execute the workflow steps one after another."""
        value = initial_value
        for step in self.steps:
            value = step(value)
        return value
