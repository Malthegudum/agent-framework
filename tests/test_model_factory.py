from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agent_framework import ModelResponse, create_language_model


def test_create_mock_language_model():
    model = create_language_model("mock", prefix="Reply:")

    response = model.generate(messages=[], tools=None)

    assert isinstance(response, ModelResponse)
    assert response.content == "Reply:"


def test_create_unknown_language_model_raises():
    import pytest

    with pytest.raises(ValueError, match="Unknown language model"):
        create_language_model("unknown")
