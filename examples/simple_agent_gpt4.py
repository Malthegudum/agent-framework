"""
Simple GPT-4 example agent.

Usage:
  - Set environment variable OPENAI_API_KEY to your OpenAI API key.
  - From the repo root (Windows pwsh):

    ```powershell
    $env:OPENAI_API_KEY = '<your-key>'
    python examples/simple_agent_gpt4.py
    ```

This script uses the framework helper `Agent.with_model` and selects GPT-4 via provider name.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agent_framework import Agent


def main():
    agent = Agent.with_model(
        name="GPT4Agent",
        model_name="gpt-4",
        system_instructions="You are a helpful assistant. Be concise and friendly.",
    )

    user_input = "Hello — introduce yourself in one short paragraph."
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])

    try:
        print(agent.run(user_input))
    except Exception as e:
        print(f"Error calling GPT-4: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
