import sys
from math import sqrt
from collections import namedtuple

import numpy as np

from src.consts import FILTERED_MIN_LEN


Vec2 = namedtuple("Vec2", "x y")


def filter_outliers(arr, bias=1.5):  # Code from circlecore/circleguard/utils.py
    """
    Returns ``arr` with outliers removed.
    Parameters
    ----------
    arr: list
        List of numbers to filter outliers from.
    bias: int
        Points in ``arr`` which are more than ``IQR * bias`` away from the first
        or third quartile of ``arr`` will be removed.
    """
    if FILTERED_MIN_LEN > len(arr):
        return arr

    q3, q1 = np.percentile(arr, [75, 25])
    iqr = q3 - q1
    lower_limit = q1 - (bias * iqr)
    upper_limit = q3 + (bias * iqr)

    return filter_by_range(arr, lower_limit, upper_limit)


def get_distance(pos_a, pos_b):
    return get_hypotenuse(pos_b.x - pos_a.x, pos_b.y - pos_a.y)


def get_hypotenuse(x, y):
    return sqrt(x ** 2 + y ** 2)


def round_cords(cords):
    return [Vec2(round(p.x), round(p.y)) for p in cords]


def get_speed(pos_a, pos_b, time_a, time_b):
    delta_time = abs(time_a - time_b)
    if delta_time == 0:
        return None

    delta_distance = get_distance(pos_a, pos_b)

    return delta_distance / delta_time


def get_speed_in_line(pos_a, pos_b, time_a, time_b):
    delta_time = abs(time_a - time_b)
    if delta_time == 0:
        return None

    delta_distance = abs(pos_a - pos_b)

    return delta_distance / delta_time


def filter_by_range(arr, lower_limit, upper_limit):
    return [x for x in arr if lower_limit < x < upper_limit]


def divide_and_round(n, d, r):
    return round(n / d, r)


def get_standard_deviation(arr, filtration=False):
    if filtration:
        arr = filter_outliers(arr)
    return np.std(arr)


def get_avg_range(arr):
    if len(arr) < 2:
        return 0

    filtered_arr = filter_outliers(arr)

    if len(filtered_arr) < 2:
        filtered_arr = arr

    return max(filtered_arr) - min(filtered_arr)


def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])

    angle = np.rad2deg((ang1 - ang2) % (2 * np.pi))
    if angle > 180:
        angle = angle - 360
    return angle


def step_to_direction_point(point, direction_point, path_len):
    delta_x = direction_point.x - point.x
    delta_y = direction_point.y - point.y

    distance = get_hypotenuse(delta_x, delta_y)
    ratio = path_len / distance
    return Vec2(point.x + ratio * delta_x, point.y + ratio * delta_y)


def calculate_path_len(path):
    path_len = 0

    for (i, point) in enumerate(path[1:], 1):
        last_point = path[i-1]
        path_len += get_hypotenuse(point.x - last_point.x, point.y - last_point.y)

    return path_len
