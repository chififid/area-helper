import numpy as np

from osrparse.utils import Mod

from src.core.objects.Timings import Timings


def get_beatmap(cl, md5, local_priority):
    try:
        if local_priority:
            b = cl.library.lookup_by_md5(md5)
        else:
            b = cl.beatmap(beatmap_md5=md5).beatmap(save=True)
    except ConnectionError:
        b = cl.library.lookup_by_md5(md5)
    except KeyError:
        b = cl.beatmap(beatmap_md5=md5).beatmap(save=True)
    return b


def get_cs(beatmap, replay):
    cs = beatmap.circle_size
    if replay.mods & Mod.HardRock:
        cs = min(10, cs * 1.3)
    elif replay.mods & Mod.Easy:
        cs /= 2

    return cs


def get_obj_radius(beatmap, replay):
    return 54.4 - 4.48 * get_cs(beatmap, replay)  # osu px


def get_ar(beatmap, replay):
    ar = beatmap.approach_rate
    if replay.mods & Mod.HardRock:
        ar = min(10, ar*1.4)
    elif replay.mods & Mod.Easy:
        ar /= 2

    return ar


def get_obj_animation_time(beatmap, replay):
    ar = get_ar(beatmap, replay)
    if ar < 5:
        time = 1200 + 600 * (5 - ar) / 5
    else:
        time = 1200 - 750 * (ar - 5) / 5
    return time  # ms


def get_od(beatmap, replay):
    easy = replay.mods & Mod.Easy
    hard_rock = replay.mods & Mod.HardRock

    return beatmap.od(easy=easy, hard_rock=hard_rock)


def get_obj_time_window(beatmap, replay, timing):
    od = get_od(beatmap, replay)

    if timing == Timings.T50:
        obj_time = int(150 + 50 * (5 - float(np.float32(od))) / 5)
    elif timing == Timings.T100:
        obj_time = (280 - 16 * od) / 2
    elif timing == Timings.T300:
        obj_time = (160 - 12 * od) / 2

    return obj_time  # ms
