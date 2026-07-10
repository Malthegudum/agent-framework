# agent-framework

This repository is an intentionally minimal foundation for building reusable AI agents, tools, and workflows in Python.

## Purpose

The goal is to provide simple building blocks for composing an agent with a language model and callable Python tools.

## Core concepts

- Agent: coordinates model calls and tool execution.
- LanguageModel: provider-independent interface for generating responses from messages.
- Tool: a Python callable exposed to an agent with a name, description, and parameter schema.
- Workflow: an ordered sequence of Python steps executed one after another.

## Real agent/tool loop

The framework internally handles the following flow:

```text
model call
-> tool request
-> function execution
-> tool result
-> second model call
-> final answer
```

The framework user does not need to implement that loop manually.

## Minimal usage example

```python
from agent_framework import Agent, Tool
from agent_framework.models import OpenAIModel


def calculate_growth(initial_value: float, final_value: float) -> float:
    return ((final_value / initial_value) - 1) * 100


growth_tool = Tool(
    name="calculate_growth",
    description="Calculate percentage growth between an initial and final value.",
    func=calculate_growth,
    parameters={
        "type": "object",
        "properties": {
            "initial_value": {"type": "number"},
            "final_value": {"type": "number"},
        },
        "required": ["initial_value", "final_value"],
    },
)

model = OpenAIModel(model="gpt-4")

agent = Agent(
    name="FinancialAnalyst",
    system_instructions=(
        "You are a financial analyst. "
        "Use tools for numerical calculations."
    ),
    model=model,
    tools=[growth_tool],
)

result = agent.run(
    "Revenue increased from 125 to 163. What was the percentage growth?"
)

print(result)
```

## Installation

From the repository root, install the package in editable mode:

```bash
pip install -e .
```

For OpenAI support, including dotenv loading for local .env files:

```bash
pip install -e ".[openai]"
```

## Running tests

```bash
pytest
```

## Running the example

```bash
python examples/calculator_agent.py
```
