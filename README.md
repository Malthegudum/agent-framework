# agent-framework

This repository is a intentionally minimal foundation for building reusable AI agents, tools, and workflows in Python.

## Purpose

The goal is to provide simple building blocks that can be imported into future projects without rebuilding basic agent functionality from scratch.

## Architecture

The package currently includes three small abstractions:

- Agent: a simple agent wrapper with a name, system instructions, optional tools, and a run method.
- Tool: a thin wrapper around a Python callable that can be executed with arguments.
- Workflow: an ordered sequence of Python steps executed one after another.

## Current limitations

This is intentionally simple and does not yet include:

- real language model integration
- memory or planning systems
- autonomous loops
- graph-based workflows

## Installation

From the repository root, install the package in editable mode:

```bash
pip install -e .
```

## Running tests

```bash
pytest
```

## Running the example

```bash
python examples/simple_agent.py
```

The package is designed to stay small and readable while you gradually add more reusable behavior.
