from collections import namedtuple

from slider import Position

from src.aim import get_aim_information
from src.core.math_utils import Vec2, angle_between


TabletData = namedtuple("TabletData", "angle offset resize")  # offset in osu px


OSU_AREA_RATIO = 4 / 3


def get_tablet_data(aim_inf):
    angle_sum = 0
    offset_sum = [0, 0]  # x, y
    resize_sum = [0, 0]  # x, y

    diff_weights_sum = 0
    resize_diff_weights_sum = [0, 0]  # x, y

    for aim_obj in aim_inf:
        weight = aim_obj.diff_weight
        diff_weights_sum += weight

        center = Vec2(Position.x_max / 2, Position.y_max / 2)

        cursor = Vec2(aim_obj.cursor_pos.x - center.x, aim_obj.cursor_pos.y - center.y)
        hit_obj = Vec2(aim_obj.hit_obj_pos.x - center.x, aim_obj.hit_obj_pos.y - center.y)

        angle = angle_between(
            (hit_obj.x, hit_obj.y),
            (cursor.x, cursor.y),
        )  # Hit turn to object counter clock
        angle_sum += angle * weight

        offset_sum[0] += (hit_obj.x - cursor.x) * weight  # From left to right
        offset_sum[1] += (hit_obj.y - cursor.y) * weight  # From top to down

        if hit_obj.x:
            resize_diff_weights_sum[0] += weight
            resize_sum[0] += (cursor.x / hit_obj.x) * weight
        if hit_obj.y:
            resize_diff_weights_sum[1] += weight
            resize_sum[1] += (cursor.y / hit_obj.y) * weight

    offset_sum[0] /= diff_weights_sum
    offset_sum[1] /= diff_weights_sum
    resize_sum[0] /= resize_diff_weights_sum[0]
    resize_sum[1] /= resize_diff_weights_sum[1]

    return TabletData(
        angle_sum / diff_weights_sum,
        Vec2(offset_sum[0], offset_sum[1] * -1),
        Vec2(resize_sum[0], resize_sum[1]),
    )


def convert_to_tablet_offset(game_offset, monitor_ratio, tablet_area):
    game_offset_relation = Vec2(
        game_offset.x / Position.x_max,
        game_offset.y / Position.y_max,
    )

    monitor_ratio_num = monitor_ratio.x / monitor_ratio.y
    if monitor_ratio_num > OSU_AREA_RATIO:
        osu_area_ratio_to_screen_y = 0.8
        osu_area_ratio_to_screen = Vec2(
            osu_area_ratio_to_screen_y * OSU_AREA_RATIO * (1 / monitor_ratio_num),
            osu_area_ratio_to_screen_y,
        )
    else:
        osu_area_ratio_to_screen_x = 0.8
        osu_area_ratio_to_screen = Vec2(
            osu_area_ratio_to_screen_x,
            osu_area_ratio_to_screen_x * (1 / OSU_AREA_RATIO) * monitor_ratio_num,
        )

    return Vec2(
        osu_area_ratio_to_screen.x * tablet_area.x * game_offset_relation.x,
        osu_area_ratio_to_screen.y * tablet_area.y * game_offset_relation.y,
    )


def give_area_config(parsed_data, additional_information):
    aim_information = get_aim_information(parsed_data.beatmap, parsed_data.replay, False)

    tablet_data = get_tablet_data(aim_information)

    print(tablet_data.angle)
    print(*tablet_data.resize)
    print(*tablet_data.offset)
    print(*convert_to_tablet_offset(
        tablet_data.offset,
        additional_information.monitor_ratio,
        additional_information.tablet_area
    ))
