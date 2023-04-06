from math import sqrt
from collections import namedtuple

from slider import beatmap
from osrparse.utils import Mod

from src.core.settings import core_settings
from src.core.objects.Timings import Timings
from src.core.beatmap import get_obj_time_window, get_obj_radius
from src.core.core import find_all_event_with_key_ranges, find_all_events_with_keys_in_timing


HitsData = namedtuple("HitsData", "hit_errors edge_hits")


def get_hits_data(replay, bm):
    hit_errors = []
    edge_hits = []

    note_time = get_obj_time_window(bm, replay, Timings.T50)
    note_size = get_obj_radius(bm, replay)

    key_ranges = find_all_event_with_key_ranges(replay.replay_data)

    hard_rock = replay.mods & Mod.HardRock
    for obj in bm.hit_objects(hard_rock=hard_rock):
        if not (isinstance(obj, beatmap.Circle) or isinstance(obj, beatmap.Slider)):
            continue

        (hit_error, is_edge_hit) = find_first_hit(obj, key_ranges, note_time, note_size)

        if hit_error:
            hit_errors.append(hit_error)
        if is_edge_hit:
            edge_hits.append(hit_error)

    return HitsData(hit_errors, edge_hits)


def find_first_hit(obj, key_ranges, note_time, note_size):
    first_hit_range = None
    first_hit_error = None
    is_edge_hit = False

    obj_time = obj.time.total_seconds() * 10**3

    (events_with_keys, i) = find_all_events_with_keys_in_timing(
        key_ranges,
        [obj_time - note_time, obj_time + note_time],
        0,
    )

    for event_with_keys in events_with_keys:
        event = event_with_keys.start.event
        distance = sqrt((event.x - obj.position.x) ** 2 + (event.y - obj.position.y) ** 2)

        if distance <= note_size:
            first_hit_range = event_with_keys
            first_hit_error = event_with_keys.start.time - obj_time

            if distance >= note_size - core_settings.EDGE_DISTANCE:
                is_edge_hit = True
            break

    while key_ranges and first_hit_range and key_ranges[0] != first_hit_range:
        del key_ranges[0]
    if key_ranges and first_hit_range and key_ranges[0] == first_hit_range:
        del key_ranges[0]

    return first_hit_error, is_edge_hit
