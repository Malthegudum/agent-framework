from agent_framework import Workflow


def test_workflow_runs_steps_in_order():
    workflow = Workflow()
    workflow.add_step(lambda value: value + 1)
    workflow.add_step(lambda value: value * 2)

    assert workflow.run(3) == 8
