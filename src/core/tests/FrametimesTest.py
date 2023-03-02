import unittest

from src.core.sliders import get_sliders
from src.core.tests.helpers import get_replay, get_beatmap
from src.core.frametimes import get_frame_times, fix_slider_frame_times, get_frame_time_num


class FrametimesTest(unittest.TestCase):
    def test_fixed_frametimes(self):
        replay = get_replay("./data/frametimes.osr")
        beatmap = get_beatmap(replay.beatmap_hash)
        sliders = get_sliders(beatmap)

        frametimes = get_frame_times(replay.replay_data)
        fixed_frametimes = fix_slider_frame_times(sliders, frametimes)

        self.assertTrue(get_frame_time_num(fixed_frametimes) == 17)

