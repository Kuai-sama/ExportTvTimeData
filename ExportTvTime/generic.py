from os import getenv
from stdiomask import getpass


from conf import settings

class Generic:
    """A class for generic methods.
    
    Methods:
        _get_credentials: Retrieves TVTime credentials.
    
    Attributes:
        _username (str): The username of the user.
        _passwd (str): The password of the user.
        _env_manager (EnvManager): An instance of the EnvManager class used to manage environment variables.
        get_credentials (tuple): A tuple containing the username and password."""
        


    def __init__(self, username: str= None, password: str = None) -> None:
        self._username = username
        self._passwd = password
        settings.OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
        self._env_manager = settings.EnvManager()
        

    def _get_credentials(self) -> tuple:
        """Retrieves TVTime credentials.

        Returns:
            tuple: A tuple containing the username and password."""

        if not getenv("TVTIME_CREDENTIALS"):
            # User input (username and password)
            user_name = input("Enter your username: ")
            password = getpass(prompt="Enter your password: ", mask="*")
        else:
            # Get the environment variable
            self._env_manager.check_if_env_is_set(settings.EnvVar.TVTIME_CREDENTIALS.value)
            tv_time_creds = getenv(settings.EnvVar.TVTIME_CREDENTIALS.value)
            try:
                user_name, password = tv_time_creds.split(";")
            except ValueError as e:
                msg = "The environment variable `TVTIME_CREDENTIALS` must be in the format `username;password`"
                raise ValueError(msg) from e
        return user_name, password

    @property
    def get_credentials(self) -> tuple:
        """Retrieves TVTime credentials from the passed variable to instance / environment or user input.

        Returns:
            tuple: A tuple containing the username and password."""
            
        if self._username and self._passwd:
            return self._username, self._passwd

        return self._get_credentials()