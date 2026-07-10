from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agent_framework import Tool


def test_tool_can_be_registered_and_executed():
    def add(a, b):
        return a + b

    tool = Tool(
        name="add",
        description="Add two numbers",
        func=add,
        parameters={
            "type": "object",
            "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
            "required": ["a", "b"],
        },
    )

    assert tool.name == "add"
    assert tool.description == "Add two numbers"
    assert tool.execute(a=2, b=3) == 5
