from pathlib import Path

from dotenv import load_dotenv

env_folder = Path(__file__).parent.parent.joinpath("conf", "env")
print(f"{env_folder = }")
 
load_dotenv(env_folder.joinpath("tvtime.env"))