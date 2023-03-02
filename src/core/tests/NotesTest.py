import unittest

from src.core.core import get_replay_data
from src.core.notes import find_all_note_hold_times
from src.core.tests.helpers import get_replay, get_beatmap


class NotesTest(unittest.TestCase):
    def test_find_all_note_hold_times(self):
        replay = get_replay("data/slider_and_notes.osr")
        replay_data = get_replay_data(replay)
        beatmap = get_beatmap(replay.beatmap_hash)
        hold_times = find_all_note_hold_times(beatmap.hit_objects(), replay_data)
        self.assertTrue(hold_times[-1] == 32 and len(hold_times) == 109)
