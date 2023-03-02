import os

from src.core.math_utils import calculate_path_len, delete_duplicates_in_list
from src.core.objects.HitObj import HitObj, HitObjType
from src.core.movements import get_nearest_cursor_pos, get_all_movements_in_timing
from src.core.timings import get_slider_velocity, get_ms_per_beat, get_inherited_beat_length
from src.core.osu_worker.timings import parse_timing_point, TimingPoint, create_additional_timing_point
from src.core.movement_path import line_approximate_movements, round_points_in_path, get_max_speed_on_path
from src.core.osu_worker.beatmap import skip_to_timings, skip_to_hit_objs, change_version, parse_slider_multiplier


def remap_and_save(parsed_data, _):
    version, new_beatmap_data = remap(parsed_data.beatmap_data, parsed_data.replay)
    file_name = f"{parsed_data.beatmap.artist} - {parsed_data.beatmap.title} ({parsed_data.beatmap.creator}) " \
                f"[{version}].osu"
    new_beatmap_file_path = os.path.join(os.path.dirname(parsed_data.beatmap_file_path), file_name)

    with open(new_beatmap_file_path, 'wb') as f:
        f.write(new_beatmap_data.encode('utf-8-sig'))


def remap(beatmap_data, replay):
    lines = beatmap_data.splitlines()

    (i, new_version) = change_version(lines, 2, "edited")
    (i, slider_multiplier) = parse_slider_multiplier(lines, i)

    i_tp = i = skip_to_timings(lines, i)
    timing_points = []
    while lines[i]:
        line = lines[i]
        timing_points.append(parse_timing_point(line))
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

        obj_relax_time = hit_obj.time - 12  # ms

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
            path = line_approximate_movements(movements, 10)

            max_speed = get_max_speed_on_path(path)
            beat_length = get_inherited_beat_length(slider_multiplier, ms_per_beat, max_speed)

            additional_timing_points.append(TimingPoint(
                hit_obj.time,
                beat_length,
            ))

            points = round_points_in_path(path)
            points = delete_duplicates_in_list(points)

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
    while lines[i]:
        last_tp = parse_timing_point(lines[i])
        if additional_timing_points and last_tp.time > additional_timing_points[0].time:
            lines.insert(i, create_additional_timing_point(additional_timing_points[0], lines[i]))
            print(lines[i])
            del additional_timing_points[0]
        i += 1

    return new_version, "\n".join(lines)