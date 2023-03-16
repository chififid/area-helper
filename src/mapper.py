import os

from src.core.objects.HitObj import HitObj, HitObjType
from src.core.objects.TimingPointType import TimingPointType
from src.core.movements import get_nearest_cursor_pos, get_all_movements_in_timing
from src.core.math_utils import calculate_path_len, round_cords
from src.core.timings import get_slider_velocity, get_ms_per_beat, get_inherited_beat_length
from src.core.osu_worker.timings import parse_timing_point, TimingPoint, create_additional_timing_point
from src.core.movement_path import line_approximate_movements, get_max_speed_on_path, \
    convert_path_to_points
from src.core.osu_worker.beatmap import skip_to_timings, skip_to_hit_objs, change_version, parse_slider_multiplier, \
    change_stack_leniency

REQUIRED_HIT_TIME = -12  # -12


def remap_and_save(parsed_data, _):
    version, new_beatmap_data = remap(parsed_data.beatmap_data, parsed_data.replay)
    file_name = f"{parsed_data.beatmap.artist} - {parsed_data.beatmap.title} ({parsed_data.beatmap.creator}) " \
                f"[{version}].osu"
    new_beatmap_file_path = os.path.join(os.path.dirname(parsed_data.beatmap_file_path), file_name)

    with open(new_beatmap_file_path, 'wb') as f:
        f.write(new_beatmap_data.encode('utf-8-sig'))


def remap(beatmap_data, replay):
    lines = beatmap_data.splitlines()

    i = change_stack_leniency(lines, 2, 0)
    (i, new_version) = change_version(lines, i, "edited")
    (i, slider_multiplier) = parse_slider_multiplier(lines, i)

    i_tp = i = skip_to_timings(lines, i)
    timing_points = []
    while lines[i]:
        line = lines[i]
        tp = parse_timing_point(line)
        if tp.type == TimingPointType.RED and not (10000 >= tp.beat_length >= 15):
            if tp.beat_length < 15:
                fixed_beat_length = 15
            else:
                fixed_beat_length = 10000
            tp = tp._replace(beat_length=fixed_beat_length)

            del lines[i]
            lines.insert(i, create_additional_timing_point(tp, line))

        timing_points.append(tp)
        i += 1

    i = skip_to_hit_objs(lines, i)

    cursor_time = 0
    replay_data_offset = 0
    lines_len = len(lines)
    additional_timing_points = []
    for line_i in range(i, lines_len):
        line = lines[line_i]

        hit_obj = HitObj.parse_from_str(line)
        if not hit_obj:
            continue
        print(hit_obj.time)

        if hit_obj.time > 16569:
            exit()

        obj_relax_time = hit_obj.time + REQUIRED_HIT_TIME  # ms

        if hit_obj.obj_type == HitObjType.Slider:
            slider_velocity = get_slider_velocity(
                slider_multiplier,
                timing_points,
                hit_obj.time,
            )
            ms_per_beat = get_ms_per_beat(timing_points, hit_obj.time)
            slider_path_delta_time = round((hit_obj.length / (slider_velocity * 100)) * ms_per_beat)
            slider_delta_time = slider_path_delta_time * hit_obj.repeat

            (movements, replay_data_offset) = get_all_movements_in_timing(
                replay.replay_data,
                [obj_relax_time, hit_obj.time + slider_delta_time],
                cursor_time,
                replay_data_offset,
            )
            cursor_time = movements[-1].time
            path = line_approximate_movements(movements, 15)

            print(path)
            max_speed = get_max_speed_on_path(path)
            print(max_speed)

            if max_speed:
                beat_length = get_inherited_beat_length(slider_multiplier, ms_per_beat, max_speed)
                additional_timing_points.append(TimingPoint(
                    hit_obj.time,
                    beat_length,
                    TimingPointType.GREEN,
                ))

            path = convert_path_to_points(path, max_speed)
            points = round_cords(path)

            hit_obj.set_slider_data([points], 1, round(calculate_path_len(points)))
            # hit_obj.set_slider_data([points], 1, round(hit_obj.length))
        else:
            (cursor_pos, replay_data_offset, cursor_time) = get_nearest_cursor_pos(
                replay.replay_data,
                obj_relax_time,
                cursor_time,
                replay_data_offset,
            )
            hit_obj.set_note_data(cursor_pos)

        new_line = hit_obj.change_osu_line(line)
        # print(new_line)
        # if line_i - i > 4:
        #     sys.exit()

        del lines[line_i]
        lines.insert(line_i, new_line)

    i = i_tp + 1
    while lines[i] and additional_timing_points:
        additional_tp = additional_timing_points[0]

        next_tp = parse_timing_point(lines[i])
        if next_tp.time > additional_tp.time:
            last_tp_line = lines[i - 1]
            last_tp = parse_timing_point(last_tp_line)

            if last_tp.time == additional_tp.time and last_tp.type == TimingPointType.GREEN:
                del lines[i - 1]
                i -= 1

            lines.insert(i, create_additional_timing_point(additional_tp, last_tp_line))
            del additional_timing_points[0]
        i += 1

    last_tp_line = lines[i - 1]
    last_tp = parse_timing_point(last_tp_line)
    while additional_timing_points:
        additional_tp = additional_timing_points[0]
        if last_tp.time == additional_tp.time and last_tp.type == TimingPointType.GREEN:
            del lines[i - 1]
            i -= 1

        lines.insert(i, create_additional_timing_point(additional_tp, last_tp_line))

        del additional_timing_points[0]
        i += 1

    print(len(lines))
    return new_version, "\n".join(lines)
