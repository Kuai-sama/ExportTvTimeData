from pathlib import Path

from dotenv import load_dotenv

env_folder = Path(__file__).parent.parent.joinpath("conf", "env")
env_file = env_folder.joinpath("tvtime.env")
 
load_dotenv(env_file)