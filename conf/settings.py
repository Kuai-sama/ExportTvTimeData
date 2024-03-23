from os import getenv
from pathlib import Path
OUTPUT_FOLDER = Path(__file__).parent.parent.joinpath("output")


class EnvManager:
    class ExceptionEnvVarNotFound(Exception):
        pass

    def __init__(self):
        self.env = None
        self.config = None

    def check_if_env_is_set(self, env_var) -> bool:
        if not getenv(env_var):
            msg = f"Can't find the environment variable `{env_var}` in the environment"
            raise self.ExceptionEnvVarNotFound(msg)
        return True

