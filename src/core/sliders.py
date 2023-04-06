from slider import beatmap

from src.core.settings import core_settings
from src.core.core import find_all_key_ranges


def get_sliders(bm):
    return [
        obj for obj in bm.hit_objects()
        if isinstance(obj, beatmap.Slider)
    ]


def find_all_slider_ranges(slider_objs):
    ranges = []

    for s in slider_objs:
        start = int(s.time.total_seconds() * 1000)
        end = int(s.end_time.total_seconds() * 1000)
        ranges.append((start, end))

    return ranges


def find_all_keys_in_slider_timing(key_ranges, timing, last_i):
    keys_in_slider_timing = []

    i = last_i
    while i < len(key_ranges) and key_ranges[i][0] < timing[1]:
        if key_ranges[i][0] > timing[0] or key_ranges[i][1] > timing[0]:
            keys_in_slider_timing.append(key_ranges[i])
        i += 1

    return keys_in_slider_timing, i


def find_all_slider_end_release_times(slider_objs, events):
    slider_end_release_times = []

    key_ranges = find_all_key_ranges(events)
    slider_ranges = find_all_slider_ranges(slider_objs)

    next_key_range_i = 0
    for slider_range in slider_ranges:
        (keys_in_slider_timing, next_key_range_i) = find_all_keys_in_slider_timing(
            key_ranges,
            slider_range,
            next_key_range_i
        )

        if keys_in_slider_timing:
            keys_in_slider_timing.sort(key=lambda key_range: (key_range[0] - slider_range[0]) ** 2)
            keys_in_slider_timing = list(filter(
                lambda timing: timing[0] == keys_in_slider_timing[0][0],
                keys_in_slider_timing
            ))
            keys_in_slider_timing.sort(key=lambda key_range: key_range[1])

            slider_end_release_time = keys_in_slider_timing[-1][1] - slider_range[1]
            if core_settings.MIN_SLIDER_END_RELEASE_TIME < slider_end_release_time < \
                    core_settings.MAX_SLIDER_END_RELEASE_TIME:
                slider_end_release_times.append(slider_end_release_time)

    return slider_end_release_times
