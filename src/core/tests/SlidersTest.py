import unittest

from src.core.core import get_replay_data
from src.core.tests.helpers import get_replay, get_beatmap
from src.core.sliders import find_all_slider_end_release_times, get_sliders


class NotesTest(unittest.TestCase):
    def test_find_all_note_hold_times(self):
        replay = get_replay("data/slider_and_notes.osr")
        replay_data = get_replay_data(replay)
        beatmap = get_beatmap(replay.beatmap_hash)
        sliders = get_sliders(beatmap)

        release_times = find_all_slider_end_release_times(sliders, replay_data)
        self.assertTrue(release_times[-1] == 28 and len(release_times) == 76)
