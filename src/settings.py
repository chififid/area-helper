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

DEBUG = get_env_var("DEBUG") == "True"

MONITOR_RATIO = int(get_env_var("MONITOR_RATIO_WIDTH")) / int(get_env_var("MONITOR_RATIO_HEIGHT"))

TABLET_AREA_WIDTH = float(get_env_var("TABLET_AREA_WIDTH"))
TABLET_AREA_HEIGHT = float(get_env_var("TABLET_AREA_HEIGHT"))
