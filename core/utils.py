"""Module for utility functions."""


def str_to_bool(value: str) -> bool:
    """
    Convert a string to a boolean value.

    This function is very useful for converting environment variables,
    which are typically strings, to boolean values.

    Args:
        value (str): The string to convert to a boolean.

    Returns:
        bool: True if the string is 'true' (case-insensitive), otherwise False.
    """
    return value.lower() == 'true'
