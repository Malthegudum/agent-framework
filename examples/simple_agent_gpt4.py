"""Example showing an agent using a Python tool through a language model."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agent_framework import Agent, Tool
from agent_framework.models import OpenAIModel


def multiply(a: float, b: float) -> float:
    return a * b


multiply_tool = Tool(
    name="multiply",
    description="Multiply two numbers.",
    func=multiply,
    parameters={
        "type": "object",
        "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"},
        },
        "required": ["a", "b"],
    },
)


def main():
    agent = Agent(
        name="Calculator",
        system_instructions=(
            "You are a calculator. "
            "Use the available tools for calculations."
        ),
        model=OpenAIModel(model="gpt-4"),
        tools=[multiply_tool],
    )

    user_input = "What is 13.7 multiplied by 8.2?"
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])

    try:
        print(agent.run(user_input))
    except Exception as exc:
        print(f"Error calling GPT-4: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
