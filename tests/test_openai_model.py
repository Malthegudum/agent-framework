from types import SimpleNamespace

from agent_framework import Message, ModelResponse, Tool, ToolCall
from agent_framework.models.openai_model import OpenAIModel


class DummyCompletions:
    def __init__(self, response):
        self._response = response
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self._response


class DummyClient:
    def __init__(self, response):
        self.chat = SimpleNamespace(completions=DummyCompletions(response))


def test_openai_model_converts_messages_and_tools():
    response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(content="Done", tool_calls=[])
            )
        ]
    )
    client = DummyClient(response)

    model = OpenAIModel.__new__(OpenAIModel)
    model._client = client
    model.model = "gpt-test"
    model._kwargs = {}

    tool = Tool(
        name="multiply",
        description="Multiply two numbers.",
        func=lambda a, b: a * b,
        parameters={
            "type": "object",
            "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
            "required": ["a", "b"],
        },
    )

    messages = [Message(role="user", content="Hello")]
    result = model.generate(messages=messages, tools=[tool])

    assert isinstance(result, ModelResponse)
    assert result.content == "Done"
    assert result.tool_calls == []
    request = client.chat.completions.calls[0]
    assert request["messages"] == [{"role": "user", "content": "Hello"}]
    assert request["tools"][0]["function"]["name"] == "multiply"


def test_openai_model_converts_tool_calls_and_tool_result_messages():
    response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content=None,
                    tool_calls=[
                        SimpleNamespace(
                            id="call-1",
                            function=SimpleNamespace(
                                name="multiply",
                                arguments='{"a": 2, "b": 3}',
                            ),
                        )
                    ],
                )
            )
        ]
    )
    client = DummyClient(response)

    model = OpenAIModel.__new__(OpenAIModel)
    model._client = client
    model.model = "gpt-test"
    model._kwargs = {}

    result = model.generate(messages=[Message(role="user", content="Hi")])

    assert result.tool_calls[0].name == "multiply"
    assert result.tool_calls[0].arguments == {"a": 2, "b": 3}

    assistant_message = Message(
        role="assistant",
        content="",
        tool_calls=[
            ToolCall(id="call-1", name="multiply", arguments={"a": 2, "b": 3})
        ],
    )
    converted_messages = model._convert_messages([assistant_message])
    assert converted_messages[0]["tool_calls"][0]["function"]["name"] == "multiply"

    converted_tool_messages = model._convert_messages(
        [Message(role="tool", content="6", tool_call_id="call-1")]
    )
    assert converted_tool_messages[0]["tool_call_id"] == "call-1"
    assert converted_tool_messages[0]["content"] == "6"


def test_openai_model_omits_tools_when_none_are_provided():
    response = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="Done", tool_calls=[]))])
    client = DummyClient(response)

    model = OpenAIModel.__new__(OpenAIModel)
    model._client = client
    model.model = "gpt-test"
    model._kwargs = {}

    model.generate(messages=[Message(role="user", content="Hi")])

    request = client.chat.completions.calls[0]
    assert "tools" not in request
