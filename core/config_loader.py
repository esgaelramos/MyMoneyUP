"""Module for loading application configuration from a YAML file."""

from typing import Dict

import yaml
from decouple import config

PATH_CONFIG_YAML = config('PATH_CONFIG_YAML', default='config.yaml')


def load_config() -> Dict[str, str]:
    """
    Load and return the application configuration based on the current env.

    Reads the configuration from a YAML file specified in PATH_CONFIG_YAML.
    The config is environment-specific, meaning it will load the settings
    based on the APP_ENV environment variable, which defaults if not set.

    Returns:
        dict: A dictionary containing the settings for the current env.
              Settings are read from the YAML file and any placeholders
              are replaced with actual values from the .env file.
    """
    # Determine the current environment. Defaults to 'default'.
    ENV = config('APP_ENV', default='default')

    # Load configuration from the YAML file.
    with open(PATH_CONFIG_YAML, "r") as file:
        config_data = yaml.safe_load(file)

    # Retrieve configuration for the current environment.
    env_config = config_data.get(ENV, {})

    # Replace placeholders with actual values from the .env file
    for key, value in env_config.items():
        env_config[key] = config(value, default=value)

    return env_config
