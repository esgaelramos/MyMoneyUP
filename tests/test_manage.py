"""
Tests for module `manage`.

In this case, we are testing the manage.py script, so we need to check
if it can be imported and if it runs correctly.
"""
import subprocess
from unittest.mock import patch

import pytest


def test_manage():
    """
    Test the importability of the main function from manage.py.

    This test checks if the main function from manage.py can be imported
    without errors, indicating the script is structured correctly.
    """
    try:
        # try importing the main function from manage.py
        from manage import main
        assert main is not None
    except Exception as e:
        pytest.fail(f"manage.py import failed: {e}")


def test_manage_raise_exception():
    """
    Test manage.py for proper error handling when Django is not importable.

    This test mocks a failed Django import to ensure that manage.py
    handles such exceptions as expected.
    """
    # use 'execute_from_command_line' and not 'import_module',
    # becasue 'import' preloads the module and we want to test!
    def mock_execute_from_command_line(*args, **kwargs):
        raise ImportError("Couldn't import Django")

    with patch("django.core.management.execute_from_command_line", mock_execute_from_command_line):  # noqa: E501
        with pytest.raises(ImportError) as execinfo:
            from manage import main
            main()

    assert "Couldn't import Django" in str(execinfo.value)


def test_manage_run():
    """
    Test the execution of manage.py's check command.

    This test executes 'manage.py check' using subprocess to ensure that
    the script runs correctly and exits without errors.
    """
    result = subprocess.run(
        ["python", "manage.py", "check"],
        capture_output=True
    )

    assert result.returncode == 0, \
        f"manage.py check failed with output: {result.stderr.decode()}"
