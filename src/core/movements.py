from collections import namedtuple

from slider import beatmap

from src.core.math_utils import get_distance, get_speed, Vec2
from src.consts import SPEED_DECREASE_FACTOR_IN, SPEED_DECREASE_FACTOR_OUT, MIN_SNAP_SPEED

Movement = namedtuple("Movement", "time x y")
AimObj = namedtuple("AimObj", "movement i")


def get_all_movements_in_timing(events, timing, time, last_i):
    movements_in_timing = []

    i = last_i
    while i < len(events) and timing[1] > (time + events[i].time_delta):
        if timing[0] is None or timing[0] < (time + events[i].time_delta):
            movements_in_timing.append(Movement(
                time + events[i].time_delta,
                events[i].x,
                events[i].y,
            ))
        time += events[i].time_delta
        i += 1

    return movements_in_timing, i


def find_all_movements_in_timing(movements, timing, last_i):
    movements_in_timing = []

    i = last_i
    while i < len(movements) and timing[1] > movements[i].time:
        if timing[0] is None or timing[0] < movements[i].time:
            movements_in_timing.append(movements[i])
        i += 1

    return movements_in_timing, i


def get_snaps(movements, obj, next_obj):
    min_speed = None
    max_speed = 0

    is_snap_aim = False

    last_current_movement = movements[0]

    snaps = []
    snap = None
    for (i, movement) in enumerate(movements[1:], 1):
        speed = get_speed(last_current_movement, movement, last_current_movement.time, movement.time)
        if not speed:
            continue
        else:
            last_current_movement = movement

        if not is_snap_aim:
            if speed > max_speed / SPEED_DECREASE_FACTOR_IN or max_speed < MIN_SNAP_SPEED:
                if speed > max_speed:
                    max_speed = speed
            else:
                is_snap_aim = True

        if is_snap_aim:  # Not else because we can get here after upper block
            if not min_speed or speed < min_speed:
                snap = AimObj(movement, i)
                min_speed = speed
            elif speed > max_speed / SPEED_DECREASE_FACTOR_OUT:
                if snap:
                    snaps.append(snap)

                # clear variables
                is_snap_aim = False
                min_speed = None
                max_speed = 0
                snap = None

    if snap:
        snaps.append(snap)

    if not snaps:
        return None, None
    else:
        return get_current_snaps(snaps, obj, next_obj)


def get_current_snaps(snaps, obj, next_obj):  # Snaps sorted by time
    current_snaps = []
    last_controversy_snap = None

    is_obj_slider = isinstance(obj, beatmap.Slider)

    obj_position = get_obj_end_position(obj)
    if is_obj_slider:
        obj_time = obj.end_time.total_seconds() * 10 ** 3
    else:
        obj_time = obj.time.total_seconds() * 10 ** 3

    if next_obj:
        next_obj_position = get_obj_end_position(next_obj)

        next_obj_time = next_obj.time.total_seconds() * 10 ** 3
        average_time = (obj_time + next_obj_time) / 2

    for snap in snaps:
        if next_obj:
            obj_dist = get_distance(snap.movement, obj_position)
            next_obj_dist = get_distance(snap.movement, next_obj_position)

            # TODO: Fix ignore slider dist
            if snap.movement.time < average_time and obj_dist < next_obj_dist:
                current_snaps.append(snap)
            elif snap.movement.time > average_time and obj_dist > next_obj_dist:
                break
        else:
            current_snaps.append(snap)

        last_controversy_snap = snap

    return current_snaps, last_controversy_snap


def get_obj_end_position(obj):
    is_slider = isinstance(obj, beatmap.Slider)

    if is_slider:
        return obj.curve(1)
    else:
        return obj.position


def get_nearest_aim_obj(movements, obj):
    nearest_obj = None
    min_distance = None

    for (i, movement) in enumerate(movements[1:], 1):
        distance = get_distance(movement, obj.position)
        if not min_distance or distance < min_distance:
            min_distance = distance
            nearest_obj = AimObj(movement, i)

    return nearest_obj


def get_nearest_cursor_pos(events, obj_time, cursor_time, last_i):
    i = last_i
    while i < len(events) and obj_time > (cursor_time + events[i].time_delta):
        cursor_time += events[i].time_delta
        i += 1

    before_mov = Movement(cursor_time, events[i-1].x, events[i-1].y)
    after_mov = Movement(cursor_time + events[i].time_delta, events[i].x, events[i].y)

    moves_delta_pos = Vec2(after_mov.x - before_mov.x, after_mov.y - before_mov.y)

    if after_mov.time - before_mov.time:
        time_ratio = (obj_time - before_mov.time) / (after_mov.time - before_mov.time)
        pos = Vec2(
            time_ratio * moves_delta_pos.x + before_mov.x,
            time_ratio * moves_delta_pos.y + before_mov.y,
        )
    else:
        pos = Vec2(before_mov.x, before_mov.y)

    return pos, i, cursor_time


def delete_same_movements(movements):
    last_movement = None

    i = 0
    while i < len(movements):
        movement = movements[i]
        if last_movement and (last_movement.time == movement.time or
                              (last_movement.x == movement.x and
                               last_movement.y == movement.y)):
            del movements[i]
        else:
            i += 1

        last_movement = movement

    return movements
