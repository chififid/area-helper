from collections import namedtuple


TimingPoint = namedtuple("TimingPoint", "time beat_length")


def parse_timing_point(point_str):
    point_data = point_str.split(",")
    return TimingPoint(
        int(point_data[0]),
        float(point_data[1])
    )


def create_additional_timing_point(additional_tp, last_tp_str):
    return f"{additional_tp.time},{additional_tp.beat_length},{last_tp_str.split(',', 2)[-1]}"
