"""
Module for utility functions.
"""

def str_to_bool(value):
    """
    Convert a string to a boolean value.

    Very useful for converting environment variables to boolean values.
    """
    return value.lower() == 'true'
