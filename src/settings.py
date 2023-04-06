import os
import sys

from dotenv import load_dotenv


def get_env_var(name):
    param = os.getenv(name)
    if not param:
        sys.exit(f"\nNot found {name} in .env file!\n")
    return param


load_dotenv()

OSU_FOLDER = get_env_var("OSU_FOLDER")

