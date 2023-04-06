from collections import namedtuple

from src.helpers import get_num
from src.parser import local_parse
from src.settings import OSU_FOLDER
from src.core.math_utils import Vec2
from src.mapper import remap_and_save
from src.tablet import give_area_config


ConfigTabletAdditionalData = namedtuple("ConfigTabletAdditionalData", "monitor_ratio tablet_area")


def run_remap(input_folder, osu_folder):
    local_parse(input_folder, osu_folder, remap_and_save)


def run_config_tablet(input_folder, osu_folder):
    monitor_ratio = get_num(
        f"Monitor aspect ratio('Width Height'): ",
        several=True,
    )
    monitor_ratio = Vec2(monitor_ratio[0], monitor_ratio[1])

    tablet_area = get_num(
        f"Tablet graph area, not ratio('Width Height'): ",
        several=True,
        another_converter=float,
    )
    tablet_area = Vec2(tablet_area[0], tablet_area[1])

    local_parse(input_folder, osu_folder, give_area_config, ConfigTabletAdditionalData(
        monitor_ratio,
        tablet_area
    ))


TabletData = namedtuple("TabletData", "angle offset resize")  # offset in osu px


INPUT_PATH = "./input/"
line = "/home/rb/PortWINE/PortProton/prefixes/DOTNET/drive_c/Program Files (x86)/OSU/"


if __name__ == "__main__":
    # run_remap(INPUT_PATH, OSU_FOLDER)
    run_config_tablet(INPUT_PATH, OSU_FOLDER)

