"""
Tests for module `core.utils`.
"""
from core.utils import str_to_bool


def test_str_to_bool_true_cases():
    """
    Test the str_to_bool function for values that should return True.
    """
    true_values = ['True', 'true', 'TRUE', 'TrUe']

    for value in true_values:
        assert str_to_bool(value) == True

def test_str_to_bool_false_cases():
    """
    Test the str_to_bool function for values that should return False.
    """
    false_values = ['False', 'false', 'FALSE', 'FaLsE', '', 'NotTrue', '123']

    for value in false_values:
        assert str_to_bool(value) == False
