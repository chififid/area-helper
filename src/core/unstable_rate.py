from src.settings import ADJUSTED_UR
from src.core.core import get_mode_divisor
from src.core.math_utils import get_standard_deviation


def get_ur(hit_errors):
    if not hit_errors:
        return 0

    return get_standard_deviation(hit_errors, ADJUSTED_UR) * 10


def convert_ur(ur, mods):
    return ur / get_mode_divisor(mods)
