import unittest

from src.core.hits import get_hits_data
from src.core.tests.helpers import get_replay, get_beatmap


class FrametimesTest(unittest.TestCase):
    def test_fixed_frametimes(self):
        replay = get_replay("./data/hits.osr")
        beatmap = get_beatmap(replay.beatmap_hash)

        hits_data = get_hits_data(replay, beatmap)
        self.assertTrue(hits_data[0][0] == -26 and hits_data[0][-1] == 111)
