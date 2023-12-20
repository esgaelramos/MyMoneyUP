"""Tests for module `core.wsgi`."""
import pytest

# wsgi is for synchronous web servers! (e.g. gunicorn?)


def test_wsgi():
    """
    This method tests the WSGI application.

    Raises:
        pytest.fail: If the WSGI application fails or is None.
    """
    try:
        from core.wsgi import application
        assert application is not None
    except Exception as e:
        pytest.fail(f"WSGI application failed: {e}")
