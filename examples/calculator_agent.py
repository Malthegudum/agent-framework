"""Example showing an agent using a Python tool through a language model."""

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


agent = Agent(
    name="Calculator",
    system_instructions=(
        "You are a calculator. "
        "Use the available tools for calculations."
    ),
    model=OpenAIModel(model="gpt-4"),
    tools=[multiply_tool],
)

print(agent.run("What is 13.7 multiplied by 8.2?"))
