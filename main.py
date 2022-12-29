import sys
import glob
from math import sqrt, degrees

from osrparse import Replay
from slider import Beatmap, Position

from src.core.math_utils import angle_between
from src.settings import OSU_FOLDER
from src.aim import get_aim_information
from src.bar import create_bar, item_done
from src.core.core import replay_validator
from src.parser import find_local_beatmap_files_by_md5

INPUT_PATH = "./input/"
line = "/home/rb/PortWINE/PortProton/prefixes/DOTNET/drive_c/Program Files (x86)/OSU/"


if __name__ == "__main__":
    paths = list(filter(
        lambda file: file.endswith(".osr"),
        glob.glob(INPUT_PATH + "*")
    ))

    with create_bar(len(paths)) as bar:
        print("Please wait")

        replays = []
        for replay_path in paths:
            with open(replay_path, "rb") as f:
                replay_string = f.read()

            replay_name = replay_path.split("/")[-1]
            replay = Replay.from_string(replay_string)

            try:
                replay_validator(replay, True)
            except Exception as e:
                item_done(bar, error_msg=f"{replay_name} - error in replay data \n{e}")
                continue

            replays.append(replay)

        md5_dict = {}
        for replay in replays:
            md5_dict[replay.beatmap_hash] = replay

        try:
            beatmap_file_paths_dict = find_local_beatmap_files_by_md5(OSU_FOLDER, md5_dict.keys())
        except Exception as e:
            sys.exit(e)

        s = 0
        for md5, replay in md5_dict.items():
            beatmap_file_path = beatmap_file_paths_dict[md5]
            with open(beatmap_file_path, 'rb') as f:
                data = f.read()
            try:
                beatmap = Beatmap.parse(data.decode('utf-8-sig'))
            except:
                item_done(bar, f'Failed to parse {beatmap_file_path}')
                continue

            aim_information = get_aim_information(beatmap, replay)

            max_weight = max([aim_obj.diff_weight for aim_obj in aim_information])

            angle_sum = 0
            offset_x_sum = 0
            offset_y_sum = 0
            resize_x_sum = 0
            resize_y_sum = 0
            diff_weights_sum = 0
            for aim_obj in aim_information:
                diff_weights_sum += aim_obj.diff_weight

                center_x = Position.x_max / 2
                center_y = Position.y_max / 2

                cursor_x = aim_obj.cursor_pos.x - center_x
                cursor_y = aim_obj.cursor_pos.y - center_y
                hit_obj_x = aim_obj.hit_obj_pos.x - center_x
                hit_obj_y = aim_obj.hit_obj_pos.y - center_y

                angle = angle_between(
                    (hit_obj_x, hit_obj_y),
                    (cursor_x, cursor_y),
                )  # Turn to object counter clock

                if angle > 180:
                    angle = angle - 360

                s += aim_obj.diff_weight / diff_weights_sum

                offset_x_sum += (hit_obj_x - cursor_x) * aim_obj.diff_weight
                offset_y_sum += (hit_obj_y - cursor_y) * aim_obj.diff_weight
                if cursor_y and cursor_x:
                    resize_x_sum += (hit_obj_x / cursor_x) * aim_obj.diff_weight
                    resize_y_sum += (hit_obj_y / cursor_y) * aim_obj.diff_weight
                angle_sum += angle * aim_obj.diff_weight

            print("Offset angle (clockwise)", -angle_sum / diff_weights_sum)
            print("Offset to the top left")
            print("X", offset_x_sum / diff_weights_sum)
            print("Y", offset_y_sum / diff_weights_sum)
            print("Resize")
            print("X", resize_x_sum / diff_weights_sum)
            print("Y", resize_y_sum / diff_weights_sum)
