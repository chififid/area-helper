import sys
import glob
from collections import namedtuple

from slider import Beatmap
from osrparse import Replay

from src.bar import create_bar, item_done
from src.core.core import replay_validator
from src.core.osu_worker.osu_db import find_local_beatmap_files_by_md5


ParsedData = namedtuple("ParsedData", "beatmap beatmap_data beatmap_file_path replay")


def local_parse(input_folder, osu_folder, callback, additional_data=None):
    paths = list(filter(
        lambda file: file.endswith(".osr"),
        glob.glob(input_folder + "*")
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
            beatmap_file_paths_dict = find_local_beatmap_files_by_md5(osu_folder, md5_dict.keys())
        except Exception as e:
            sys.exit(e)

        for md5, replay in md5_dict.items():
            beatmap_file_path = beatmap_file_paths_dict[md5]
            with open(beatmap_file_path, 'rb') as f:
                data = f.read()
            try:
                beatmap = Beatmap.parse(data.decode('utf-8-sig'))
                beatmap_data = data.decode('utf-8-sig')
            except:
                item_done(bar, f'Failed to parse {beatmap_file_path}')
                continue

            callback(ParsedData(
                beatmap,
                beatmap_data,
                beatmap_file_path,
                replay,
            ), additional_data)

            item_done(bar)
