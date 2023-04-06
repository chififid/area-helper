from src.core.objects.TimingPointType import TimingPointType


def get_slider_velocity(slider_multiplier, timing_points, slider_start_time):
    i = 0
    while i < len(timing_points) and timing_points[i].time <= slider_start_time:
        i += 1

    timing_point = timing_points[i - 1]
    beat_length = timing_point.beat_length
    if timing_point.type == TimingPointType.RED:
        slider_velocity = slider_multiplier
    else:
        slider_velocity = slider_multiplier * (-100 / beat_length)

    return slider_velocity


def get_ms_per_beat(timing_points, slider_start_time):
    result = None
    for timing_point in timing_points:
        if timing_point.time > slider_start_time:
            break

        beat_length = timing_point.beat_length
        if beat_length > 0:
            result = beat_length

    return result


def get_inherited_beat_length(slider_multiplier, ms_per_beat, speed):
    # speed = (100 / ms_per_beat) * (slider_velocity)
    # insert slider_velocity ->
    # speed = (100 / ms_per_beat) * (slider_multiplier * (-100 / beat_length))
    # speed = (100 * slider_multiplier * -100) / (beat_length * ms_per_beat)
    # multiply by ms_per_beat and divide by speed ->
    # beat_length = (-10000 * slider_multiplier) / (speed * ms_per_beat)

    return (-10000 * slider_multiplier) / (speed * ms_per_beat)
