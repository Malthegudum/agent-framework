from pathlib import Path
import sys

import pytest

from agent_framework import Agent, Message, ModelResponse, Tool, ToolCall


class FakeModel:
    def __init__(self, responses=None):
        self.responses = responses or []
        self.calls = []

    def generate(self, messages, tools=None):
        self.calls.append((messages, tools))
        if not self.responses:
            raise AssertionError("No response configured for fake model")
        return self.responses.pop(0)


def test_agent_returns_model_content():
    model = FakeModel([ModelResponse(content="Hello")])
    agent = Agent(name="Helper", system_instructions="Be helpful", model=model)

    assert agent.run("Hi") == "Hello"
    assert len(model.calls) == 1
    assert model.calls[0][0][0].role == "system"
    assert model.calls[0][0][0].content == "Be helpful"
    assert model.calls[0][0][1].role == "user"
    assert model.calls[0][0][1].content == "Hi"


def test_agent_executes_tool_loop():
    def multiply(a, b):
        return a * b

    tool = Tool(
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

    class ScriptedModel(FakeModel):
        def generate(self, messages, tools=None):
            self.calls.append((messages, tools))
            if len(self.calls) == 1:
                return ModelResponse(
                    tool_calls=[
                        ToolCall(
                            id="call-1",
                            name="multiply",
                            arguments={"a": 2, "b": 3},
                        )
                    ]
                )

            tool_messages = [message for message in messages if message.role == "tool"]
            assert len(tool_messages) == 1
            assert tool_messages[0].tool_call_id == "call-1"
            assert tool_messages[0].content == "6"
            return ModelResponse(content="The result is 6.")

    model = ScriptedModel()
    agent = Agent(name="Calculator", system_instructions="Use tools", tools=[tool], model=model)

    assert agent.run("Calculate 2 * 3") == "The result is 6."
    assert len(model.calls) == 2


def test_agent_raises_for_unknown_tool():
    model = FakeModel(
        [
            ModelResponse(
                tool_calls=[
                    ToolCall(id="call-1", name="does_not_exist", arguments={})
                ]
            )
        ]
    )
    agent = Agent(name="Helper", model=model)

    with pytest.raises(ValueError, match="does_not_exist"):
        agent.run("Hi")


def test_agent_raises_when_max_iterations_exceeded():
    class RepeatingToolModel(FakeModel):
        def generate(self, messages, tools=None):
            self.calls.append((messages, tools))
            return ModelResponse(
                tool_calls=[
                    ToolCall(id="call-1", name="multiply", arguments={"a": 2, "b": 3})
                ]
            )

    def multiply(a, b):
        return a * b

    tool = Tool(
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
    model = RepeatingToolModel()
    agent = Agent(name="Calculator", tools=[tool], model=model, max_iterations=3)

    with pytest.raises(RuntimeError, match="maximum iterations"):
        agent.run("Hi")


