import os
import sys

from dotenv import load_dotenv


def get_env_var(name):
    param = os.getenv(name)
    if not param:
        sys.exit(f"\nNot found {name} in .env file!\n")
    return param


load_dotenv()

ROUND_DIGIT_COUNT = int(get_env_var("ROUND_DIGIT_COUNT"))
EDGE_DISTANCE = int(get_env_var("EDGE_DISTANCE"))
ADJUSTED_UR = get_env_var("ADJUSTED_UR") == "True"
OSU_FOLDER = get_env_var("OSU_FOLDER")
