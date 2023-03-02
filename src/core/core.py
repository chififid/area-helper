from collections import namedtuple

from slider import beatmap
from osrparse.utils import Mod
from osrparse import utils, GameMode

KeyRange = namedtuple("KeyRange", "start end")
KeyRangeEvent = namedtuple("KeyRangeEvent", "time event")


def parse_optional(conversion):
    def func(cs):
        try:
            return conversion(cs)
        except:
            return None

    return func


def replay_validator(replay, rx):
    if replay.mode != GameMode.STD:
        raise Exception("Not std replay")

    if (not rx) and len(find_all_key_ranges(replay.replay_data)) < 10:
        raise Exception("Unable to get enough data")


def get_mode_divisor(mods):
    if mods & (Mod.DoubleTime | Mod.Nightcore):
        return 1.5
    elif mods & Mod.HalfTime:
        return 0.75
    return 1


def get_replay_data(replay):
    replay_data = replay.replay_data
    delta_time = 0
    while replay_data[0].x == 256 and replay_data[0].y == -500:
        delta_time += replay_data[0].time_delta
        del replay_data[0]
    replay_data[0].time_delta += delta_time
    return replay_data


def find_all_event_with_key_ranges(events):
    ranges = []

    last = {}
    time = 0

    keys = [utils.Key.K1, utils.Key.K2]
    for event in events:
        time += event.time_delta

        pressed_keys = event.keys
        if not ((utils.Key.M1 | utils.Key.K1) - pressed_keys):
            pressed_keys -= utils.Key.M1
        if not ((utils.Key.M2 | utils.Key.K2) - pressed_keys):
            pressed_keys -= utils.Key.M2

        for k in keys:
            if pressed_keys & k:
                if k not in last.keys():
                    last[k] = KeyRangeEvent(time, event)
            elif k in last.keys():
                ranges.append(KeyRange(last[k], KeyRangeEvent(time, event)))
                last.pop(k)

    return ranges


def find_all_key_ranges(events):
    ranges = find_all_event_with_key_ranges(events)

    return [(key_range.start.time, key_range.end.time) for key_range in ranges]


def find_all_events_with_keys_in_timing(key_ranges, timing, last_i):
    keys_in_note_timing = []

    i = last_i
    while i < len(key_ranges) and timing[1] > key_ranges[i].start.time:
        if timing[0] is None or timing[0] < key_ranges[i].start.time:
            keys_in_note_timing.append(key_ranges[i])
        i += 1

    return keys_in_note_timing, i


def find_all_keys_in_timing(key_ranges, timing, last_i):
    ranges = find_all_events_with_keys_in_timing(key_ranges, timing, last_i)

    return [(key_range.start.time, key_range.end.time) for key_range in ranges[0]], ranges[1]


def check_current_obj(obj):
    return isinstance(obj, beatmap.Circle) or isinstance(obj, beatmap.Slider)


def add_optional_conversions(client):
    for key, value in client._beatmap_conversions.items():
        if key in optional_params:
            client._beatmap_conversions[key] = parse_optional(value)


optional_params = [
    "approved_date",
    "last_update",
    "genre",
    "language",
]
