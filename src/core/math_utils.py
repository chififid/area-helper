from math import sqrt

import numpy as np

from src.consts import FILTERED_MIN_LEN


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
    return sqrt(
        (pos_b.x - pos_a.x) ** 2 +
        (pos_b.y - pos_a.y) ** 2
    )


def get_speed(pos_a, pos_b, time_a, time_b):
    delta_time = time_a - time_b
    if delta_time == 0:
        return None

    delta_distance = get_distance(pos_a, pos_b)

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
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))
