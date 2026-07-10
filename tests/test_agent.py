from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agent_framework import Agent, Tool


def test_agent_has_name_and_runs_with_tools():
    def greet(name):
        return f"Hello, {name}"

    tool = Tool(name="greet", description="Say hello", func=greet)
    agent = Agent(name="Helper", system_instructions="Be helpful", tools=[tool])

    result = agent.run("Ada")

    assert "Helper" in result
    assert "greet" in result
