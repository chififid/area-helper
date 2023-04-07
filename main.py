from collections import namedtuple

from src.consts import INPUT_PATH
from src.parser import local_parse
from src.core.math_utils import Vec2
from src.tablet import give_area_config
from src.core.settings import core_settings
from src.settings import OSU_FOLDER, MONITOR_RATIO, TABLET_AREA_WIDTH, TABLET_AREA_HEIGHT


ConfigTabletAdditionalData = namedtuple("ConfigTabletAdditionalData", "monitor_ratio tablet_area")


def run_config_tablet(input_folder, osu_folder):
    monitor_ratio = MONITOR_RATIO
    tablet_area = Vec2(TABLET_AREA_WIDTH, TABLET_AREA_HEIGHT)

    local_parse(input_folder, osu_folder, give_area_config, ConfigTabletAdditionalData(
        monitor_ratio,
        tablet_area
    ))


if __name__ == "__main__":
    core_settings.re_init(osu_folder=OSU_FOLDER)

    run_config_tablet(INPUT_PATH, OSU_FOLDER)

