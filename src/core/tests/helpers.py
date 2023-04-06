import os

from slider import Beatmap
from osrparse import Replay
from dotenv import load_dotenv

from src.core.settings import core_settings
from src.core.osu_worker.osu_db import find_local_beatmap_files_by_md5


def init_osu_db():
    load_dotenv()
    osu_folder = os.getenv("OSU_FOLDER")
    core_settings.re_init(osu_folder=osu_folder)


def get_replay(file_path):
    with open(file_path, "rb") as f:
        replay_string = f.read()

    replay = Replay.from_string(replay_string)
    return replay


def get_beatmap(md5):
    init_osu_db()

    beatmap_file_paths_dict = find_local_beatmap_files_by_md5(core_settings.OSU_FOLDER, [md5])
    beatmap_file_path = beatmap_file_paths_dict[md5]

    with open(beatmap_file_path, 'rb') as f:
        data = f.read()

    beatmap = Beatmap.parse(data.decode('utf-8-sig'))
    return beatmap
