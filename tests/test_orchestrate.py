"""Test cases for the orchestrate module."""

import pytest

from gator import constants
from gator import orchestrate
from gator import report


@pytest.fixture
def reset_results_dictionary():
    """Reset the state of the results dictionary."""
    report.reset()


@pytest.mark.parametrize(
    "commandline_arguments",
    [
        (["--json", "CHECK"]),
        (["--json", "--nowelcome", "CHECK"]),
        (["--nowelcome", "CHECK"]),
    ],
)
def test_verify_arguments(commandline_arguments):
    """Check if the verification of arguments works from orchestrate."""
    parsed_arguments, remaining_arguments = orchestrate.parse_arguments(
        commandline_arguments
    )
    verification_status = orchestrate.verify_arguments(parsed_arguments)
    assert parsed_arguments is not None
    assert verification_status is True


@pytest.mark.parametrize(
    "commandline_arguments, expected_verification, action_count",
    [
        (["check_commits"], True, 1),
        (["--json", "CHECK"], True, 1),
        (["--json", "--nowelcome", "CHECK"], True, 0),
        (["--nowelcome", "CHECK"], True, 0),
        (["--nowelcome", "--checkerdir", "WRONG", "CHECK"], False, 3),
    ],
)
def test_get_actions(commandline_arguments, expected_verification, action_count):
    """Check if the generation of preliminary actions works from orchestrate."""
    parsed_arguments, remaining_arguments = orchestrate.parse_arguments(
        commandline_arguments
    )
    verification_status = orchestrate.verify_arguments(parsed_arguments)
    assert parsed_arguments is not None
    assert verification_status is expected_verification
    needed_actions = orchestrate.get_actions(parsed_arguments, verification_status)
    assert len(needed_actions) == action_count


def test_perform_actions_no_parameters_welcome(capsys):
    """Check to see if perform can invoke welcome action with no parameters."""
    actions = []
    actions.append([orchestrate.DISPLAY, "welcome_message", []])
    orchestrate.perform_actions(actions)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "GatorGrader" in captured.out
    assert counted_newlines == 4
    assert captured.err == ""


def test_perform_actions_no_parameters_incorrect(capsys):
    """Check to see if perform can invoke welcome action with no parameters."""
    actions = []
    actions.append([orchestrate.DISPLAY, "incorrect_message", []])
    orchestrate.perform_actions(actions)
    captured = capsys.readouterr()
    counted_newlines = captured.out.count("\n")
    assert "Incorrect" in captured.out
    assert counted_newlines == 2
    assert captured.err == ""


# pylint: disable=unused-argument
def test_perform_actions_single_parameter_exit(capsys):
    """Check to see if perform can invoke exit actions with a parameter."""
    actions = []
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        actions.append([orchestrate.RUN, "run_exit", [constants.arguments.Incorrect]])
        orchestrate.perform_actions(actions)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2
