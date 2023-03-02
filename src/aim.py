from collections import namedtuple

from osrparse.utils import Mod
from slider import beatmap, Position

from src.core.math_utils import get_distance
from src.core.objects.Timings import Timings
from src.core.core import check_current_obj, get_replay_data
from src.core.beatmap import get_obj_animation_time, get_obj_time_window
from src.core.movements import get_all_movements_in_timing, get_snaps, get_nearest_obj


AimOffset = namedtuple("AimOffset", "hit_obj_pos cursor_pos diff_weight")


def get_aim_information(bm, replay):
    result = []

    time = 0
    next_event_i = 0
    first_event_i_in_last_obj_timing = 0

    prev_aim_obj = None

    hard_rock = replay.mods & Mod.HardRock
    hit_objs = bm.hit_objects(hard_rock=hard_rock)
    replay_data = get_replay_data(replay)
    for (obj_i, obj) in enumerate(hit_objs):
        next_obj = None
        if obj_i + 1 < len(hit_objs):
            next_obj = hit_objs[obj_i + 1]

        if not check_current_obj(obj):
            continue

        animation_time = get_obj_animation_time(bm, replay)
        window_timing = get_obj_time_window(bm, replay, Timings.T50)

        obj_time = obj.time.total_seconds() * 10 ** 3

        timing = [obj_time - animation_time]

        obj_end_time = obj_time
        if isinstance(obj, beatmap.Slider):
            obj_end_time = obj.end_time.total_seconds() * 10 ** 3

        if next_obj:
            next_obj_time = next_obj.time.total_seconds() * 10 ** 3
            timing.append(min(obj_end_time + window_timing * 2, next_obj_time))
        else:
            timing.append(obj_end_time + window_timing)

        replay_data_offset = first_event_i_in_last_obj_timing + next_event_i
        (movements, event_i_after_obj_timing) = get_all_movements_in_timing(
            replay_data,
            timing,
            time,
            replay_data_offset,
        )

        first_event_i_in_last_obj_timing = event_i_after_obj_timing - len(movements)

        (current_snaps, max_snap) = get_snaps(movements, obj, next_obj)

        if max_snap:
            time = max_snap.movement.time
            next_event_i = max_snap.i

        if current_snaps:
            aim_obj = current_snaps[0]
        elif not current_snaps:
            aim_obj = get_nearest_obj(movements, obj)
            if (max_snap and aim_obj.movement.time > time) or not max_snap:
                time = aim_obj.movement.time
                next_event_i = aim_obj.i

        if prev_aim_obj:
            diff_weight = get_diff_weight(prev_aim_obj, obj)
            result.append(AimOffset(
                obj.position,
                Position(aim_obj.movement.x, aim_obj.movement.y),
                diff_weight,
            ))

        prev_aim_obj = aim_obj

    return result


def get_diff_weight(prev_aim_obj, obj):
    distance = get_distance(obj.position, prev_aim_obj.movement)
    return distance
