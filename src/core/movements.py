from collections import namedtuple

from slider import beatmap

from src.core.math_utils import get_distance, get_speed
from src.consts import SPEED_DECREASE_FACTOR, MIN_SNAP_SPEED, FORCE_SNAP_DISTANCE

Movements = namedtuple("Movement", "time x y")
AimObj = namedtuple("AimObj", "movement i")


def find_all_movements_in_timing(events, timing, time):
    movements_in_timing = []

    i = 0
    while i < len(events) and timing[1] > (time + events[i].time_delta):
        if timing[0] is None or timing[0] < (time + events[i].time_delta):
            movements_in_timing.append(Movements(
                time + events[i].time_delta,
                events[i].x,
                events[i].y,
            ))
        time += events[i].time_delta
        i += 1

    return movements_in_timing, i


def get_snaps(movements, obj, next_obj):
    min_speed = None
    max_speed = 0

    is_snap_aim = False

    last_current_movement = movements[0]

    snaps = []
    snap = None
    for i in range(1, len(movements)):
        movement = movements[i]

        delta_distance = get_distance(last_current_movement, movement)
        speed = get_speed(last_current_movement, movement, last_current_movement.time, movement.time)
        if not speed:
            continue
        else:
            last_current_movement = movement

        if not is_snap_aim:
            if (speed > max_speed / SPEED_DECREASE_FACTOR and delta_distance > FORCE_SNAP_DISTANCE) \
                    or max_speed < MIN_SNAP_SPEED:
                if speed > max_speed:
                    max_speed = speed
            else:
                is_snap_aim = True

        if is_snap_aim:  # Not else because we can get here after upper block
            if delta_distance < FORCE_SNAP_DISTANCE:
                snap = AimObj(movement, i)
                snaps.append(snap)

                snap = None
            elif not min_speed or speed < min_speed:
                snap = AimObj(movement, i)
                min_speed = speed
            elif speed > max_speed / SPEED_DECREASE_FACTOR and delta_distance > FORCE_SNAP_DISTANCE:
                if snap:
                    snaps.append(snap)

                min_speed = None
                max_speed = 0
                is_snap_aim = False
                snap = None

    if is_snap_aim and snap:
        snaps.append(snap)

    if not snaps:
        return None, None
    else:
        return get_current_snaps(snaps, obj, next_obj)


def get_current_snaps(snaps, obj, next_obj):
    current_snaps = []
    max_snap = None

    is_slider = isinstance(obj, beatmap.Slider)
    if is_slider:
        obj_time = obj.end_time.total_seconds() * 10 ** 3
    else:
        obj_time = obj.time.total_seconds() * 10 ** 3

    if next_obj:
        next_obj_time = next_obj.time.total_seconds() * 10 ** 3
        average_time = (obj_time + next_obj_time) / 2

    for snap in snaps:
        if next_obj:
            if not is_slider:
                obj_dist = get_distance(snap.movement, obj.position)
                next_obj_dist = get_distance(snap.movement, next_obj.position)

            # TODO: Fix ignore slider dist
            if snap.movement.time < average_time and \
                    (is_slider or (not is_slider and obj_dist < next_obj_dist)):
                current_snaps.append(snap)
            elif snap.movement.time > average_time and \
                    (is_slider or (not is_slider and obj_dist > next_obj_dist)):
                continue  # Snapped to next obj
        else:
            current_snaps.append(snap)

        if not max_snap or max_snap.movement.time < snap.movement.time:
            max_snap = snap

    return current_snaps, max_snap


def get_nearest_obj(movements, obj):
    nearest_obj = None
    min_distance = None

    for i in range(1, len(movements)):
        movement = movements[i]

        distance = get_distance(movement, obj.position)
        if not min_distance or distance < min_distance:
            min_distance = distance
            nearest_obj = AimObj(movement, i)

    return nearest_obj
