from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agent_framework import Agent, Tool, Workflow


def greet(name: str) -> str:
    return f"Hello, {name}!"


tool = Tool(name="greet", description="Say hello", func=greet)
agent = Agent(name="SimpleAgent", system_instructions="Be friendly", tools=[tool])
workflow = Workflow()
workflow.add_step(lambda value: agent.run(value))
workflow.add_step(lambda value: value.upper())

if __name__ == "__main__":
    print(workflow.run("Ada"))
