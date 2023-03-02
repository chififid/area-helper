import os
from struct import unpack_from
from collections import namedtuple

from termcolor import colored
from numpy.compat import unicode

from src.consts import OSU_DB_FILE, OSU_DB_SONGS


Beatmap = namedtuple("Beatmap", "md5 folder file")


def parse_num(db, offset_n, length):
    type_map = {1: "B", 2: "H", 4: "I", 8: "Q"}
    num_type = type_map[length]
    val = unpack_from(num_type, db, offset_n)[0]
    return val, offset_n + length


def parse_string(db, offset_n):
    existence = unpack_from("b", db, offset_n)[0]
    if existence == 0x00:
        return "", offset_n + 1
    elif existence == 0x0b:
        # decode ULEB128
        length = 0
        shift = 0
        offset_n += 1
        while True:
            val = unpack_from("B", db, offset_n)[0]
            length |= ((val & 0x7F) << shift)
            offset_n += 1
            if (val & (1 << 7)) == 0:
                break
            shift += 7

        string = unpack_from(str(length)+"s", db, offset_n)[0]
        offset_n += length

        try:
            unicode_s = unicode(string, "utf-8")
        except UnicodeDecodeError:
            raise Exception("Could not parse UTF-8 string!")

        return unicode_s, offset_n


def parse_beatmap(db, offset_n):
    for i in range(7):  # Skip useless fields
        _, offset_n = parse_string(db, offset_n)

    # useful fields
    md5, offset_n = parse_string(db, offset_n)
    file, offset_n = parse_string(db, offset_n)

    # Skip useless fields
    offset_n += 39

    for i in range(4):
        num_pairs, offset_n = parse_num(db, offset_n, 4)
        offset_n += 14 * num_pairs

    offset_n += 12

    num_points, offset_n = parse_num(db, offset_n, 4)
    offset_n += 17 * num_points

    offset_n += 23
    for i in range(2):
        _, offset_n = parse_string(db, offset_n)
    offset_n += 2
    _, offset_n = parse_string(db, offset_n)
    offset_n += 10
    folder, offset_n = parse_string(db, offset_n)
    offset_n += 18

    # return
    bm = Beatmap(md5, folder, file)
    return bm, offset_n


def find_local_beatmap_files_by_md5(osu_folder, md5_list):
    try:
        with open(osu_folder + OSU_DB_FILE, "rb") as db_f:
            database = db_f.read()
    except OSError:
        raise Exception("Could not open osu folder!")

    offset = 17  # Skip useless fields
    try:
        _, offset = parse_string(database, offset)
        num_beatmaps, offset = parse_num(database, offset, 4)
    except Exception as e:
        raise Exception("Broken osu db file!\nError:\n" + e)

    files = {}
    for _ in range(num_beatmaps):
        try:
            beatmap, offset = parse_beatmap(database, offset)
        except Exception as e:
            print(colored(e, "yellow"))
            continue

        if beatmap.md5 in md5_list:
            path = os.path.join(
                osu_folder,
                OSU_DB_SONGS,
                beatmap.folder,
                beatmap.file,
            )
            files[beatmap.md5] = path

    return files
