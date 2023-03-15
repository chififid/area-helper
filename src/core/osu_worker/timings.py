import math
from collections import namedtuple

from src.core.objects.TimingPointType import TimingPointType


TimingPoint = namedtuple("TimingPoint", "time beat_length type")


def parse_timing_point(point_str):
    point_data = point_str.split(",")

    return TimingPoint(
        math.trunc(float(point_data[0])),
        float(point_data[1]),
        TimingPointType(int(point_data[-2])),
    )


def create_additional_timing_point(additional_tp, last_tp_str):
    last_str_data = last_tp_str.split(',', 2)[-1].rsplit(',', 2)
    return f"{additional_tp.time},{additional_tp.beat_length},{last_str_data[0]},{additional_tp.type.value}," \
           f"{last_str_data[-1]}"
