import unittest

from src.core.core import get_replay_data
from src.core.tests.helpers import get_replay, get_beatmap
from src.core.movements import get_all_movements_in_timing, get_snaps, get_nearest_cursor_pos


class MovementsTest(unittest.TestCase):
    def test_get_all_movements_in_timing(self):
        replay = get_replay("./data/movements.osr")
        replay_data = get_replay_data(replay)
        (movements, i) = get_all_movements_in_timing(replay_data, [4000, 5234], 0, 0)
        self.assertTrue(movements[0].time == 4016 and movements[-1].time == 5229 and len(movements) == 104)
        (movements, i) = get_all_movements_in_timing(replay_data, [5000, 6234], movements[-1].time, i)
        self.assertTrue(movements[0].time == 5238 and movements[-1].time == 6230 and len(movements) == 74)

    def test_get_snaps(self):
        replay = get_replay("./data/movements.osr")
        replay_data = get_replay_data(replay)
        beatmap = get_beatmap(replay.beatmap_hash)
        hit_objects = beatmap.hit_objects()

        # Check flow aim
        (movements, i) = get_all_movements_in_timing(replay_data, [193856, 193988], 0, 0)
        (current_snaps, max_snap) = get_snaps(movements, hit_objects[1316], hit_objects[1317])
        self.assertTrue(not current_snaps)

        # Check snap aim
        (movements, i) = get_all_movements_in_timing(replay_data, [129154, 130047], 0, 0)
        (current_snaps, max_snap) = get_snaps(movements, hit_objects[863], hit_objects[864])
        self.assertTrue(len(current_snaps) == 1 and current_snaps[0].movement.time == 129228)

    def test_get_nearest_cursor_pos(self):
        replay = get_replay("./data/movements.osr")
        replay_data = get_replay_data(replay)

        (pos, i, cursor_time) = get_nearest_cursor_pos(replay_data, 129228, 0, 0)
        self.assertTrue(cursor_time == 129219 and round(pos.x) == 233 and round(pos.y) == -4)
        (pos, i, cursor_time) = get_nearest_cursor_pos(replay_data, 129439, cursor_time, i)
        self.assertTrue(cursor_time == 129433 and round(pos.x) == 117 and round(pos.y) == 400)

