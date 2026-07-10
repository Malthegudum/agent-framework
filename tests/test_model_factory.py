from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agent_framework import create_language_model


def test_create_mock_language_model():
    model = create_language_model("mock", prefix="Reply:")

    assert model.generate("Hello") == "Reply: Hello"


def test_create_unknown_language_model_raises():
    import pytest

    with pytest.raises(ValueError, match="Unknown language model"):
        create_language_model("unknown")
