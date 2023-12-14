import yaml
from decouple import config

PATH_CONFIG_YAML = config('PATH_CONFIG_YAML', default='config.yaml')

def load_config():
    # Determina el entorno actual. Por defecto es 'default'.
    ENV = config('APP_ENV', default='default')

    # Carga la configuración desde el archivo YAML.
    with open(PATH_CONFIG_YAML, "r") as file:
        config_data = yaml.safe_load(file)

    # Obtiene la configuración para el entorno actual.
    env_config = config_data.get(ENV, {})

    # Reemplaza los placeholders con los valores reales del archivo .env
    for key, value in env_config.items():
        env_config[key] = config(value, default=value)

    return env_config
