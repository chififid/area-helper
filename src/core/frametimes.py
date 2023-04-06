from src.core.settings import core_settings
from src.core.math_utils import divide_and_round
from src.core.sliders import find_all_slider_ranges


def get_frame_times(events):
    return [event.time_delta for event in events]


def fix_slider_frame_times(slider_objs, frame_times):
    fixed_frame_times = []

    slider_ranges = find_all_slider_ranges(slider_objs)

    i = 0
    time = 0
    in_slider = False
    while i < len(frame_times):
        time_delta = frame_times[i]
        time += time_delta

        while slider_ranges and slider_ranges[0][1] < time:
            del slider_ranges[0]

        if not slider_ranges or slider_ranges[0][0] > time:
            if in_slider:  # First frame after slider
                in_slider = False

                i += 1
                if i < len(frame_times):
                    time += frame_times[i]

                try:
                    del fixed_frame_times[-1]
                    del fixed_frame_times[-1]
                except IndexError:
                    pass  # It's normal situation
            else:
                fixed_frame_times.append(time_delta)
        else:
            in_slider = True

        i += 1

    return fixed_frame_times


def divide_frame_times(frame_times, divisor):
    return [divide_and_round(frame_time, divisor, core_settings.ROUND_DIGIT_COUNT) for frame_time in frame_times]


def get_frame_time_num(frame_times):
    max_count = 0
    frame_time = 0
    for i in frame_times:
        count = frame_times.count(i)
        if count > max_count and frame_time != i:
            max_count = count
            frame_time = i
    return frame_time
