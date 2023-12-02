"""
Tests for module `manage`.

In this case, we are testing the manage.py script, so we need to check
if it can be imported and if it runs correctly.
"""
import pytest
import subprocess

from unittest.mock import patch


def test_manage():
    try:
        # Intenta importar la función principal de manage.py
        from manage import main
        assert main is not None
    except Exception as e:
        pytest.fail(f"manage.py import failed: {e}")


def test_manage_raise_exception():
    # use 'execute_from_command_line' and not 'import_module', becasue 'import' preloads the module and we want to test!
    def mock_execute_from_command_line(*args, **kwargs):
        raise ImportError("Couldn't import Django")

    with patch("django.core.management.execute_from_command_line", mock_execute_from_command_line):
        with pytest.raises(ImportError) as execinfo:
            from manage import main
            main()

    assert "Couldn't import Django" in str(execinfo.value)


def test_manage_run():
    result = subprocess.run(["python", "manage.py", "check"], capture_output=True)
    assert result.returncode == 0, f"manage.py check failed with output: {result.stderr.decode()}"
