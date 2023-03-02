from slider import beatmap

from src.consts import MAX_NOTE_HOLD_TIME
from src.core.core import find_all_keys_in_timing, find_all_event_with_key_ranges


def find_all_note_hold_times(objs, events):
    notes_hold_time = []

    key_ranges = find_all_event_with_key_ranges(events)

    next_key_range_i = 0
    for obj_i in range(len(objs) - 1):
        if isinstance(objs[obj_i], beatmap.Circle):
            note_time = objs[obj_i].time.total_seconds() * 10**3
            if obj_i > 0:
                prev_obj_time = objs[obj_i - 1].time.total_seconds() * 1000
            else:
                prev_obj_time = 0
            if obj_i + 1 < len(objs):
                next_obj_time = objs[obj_i + 1].time.total_seconds() * 1000
            else:
                next_obj_time = note_time + 10**3 * 5

            timing = (
                (prev_obj_time + note_time) / 2,
                (next_obj_time + note_time) / 2,
            )
            (keys_in_note_timing, next_key_range_i) = find_all_keys_in_timing(key_ranges, timing, next_key_range_i)

            if keys_in_note_timing:
                keys_in_note_timing.sort(key=lambda key_range: (key_range[0] - note_time) ** 2)
                min_timing = keys_in_note_timing[0]

                note_hold_time = min_timing[1] - min_timing[0]

                if note_hold_time < MAX_NOTE_HOLD_TIME:
                    notes_hold_time.append(min_timing[1] - min_timing[0])

    return notes_hold_time
