import unittest

from osrparse import ReplayEventOsu

from src.core.core import find_all_event_with_key_ranges, KeyRange, KeyRangeEvent
from src.core.tests.helpers import get_replay


class CoreTest(unittest.TestCase):
    def test_find_all_event_with_key_ranges(self):
        replay = get_replay("data/key_ranges.osr")

        expected_result = [  # First and last key range
            KeyRange(
                KeyRangeEvent(24, ReplayEventOsu(None, 73.77778, 186.2222, None)),
                KeyRangeEvent(36, ReplayEventOsu(None, 74.66666, 187.5556, None)),
            ),
            KeyRange(
                KeyRangeEvent(8897, ReplayEventOsu(None, -8.444445, 148.8889, None)),
                KeyRangeEvent(9317, ReplayEventOsu(None, 216.4444, 142.2222, None)),
            ),
        ]
        event_with_key_ranges = find_all_event_with_key_ranges(replay.replay_data)

        is_succeeded = key_range_events_equal(expected_result[0].start, event_with_key_ranges[0].start) and \
            key_range_events_equal(expected_result[0].end, event_with_key_ranges[0].end) and \
            key_range_events_equal(expected_result[-1].start, event_with_key_ranges[-1].start) and \
            key_range_events_equal(expected_result[-1].end, event_with_key_ranges[-1].end)

        self.assertTrue(is_succeeded)


def key_range_events_equal(x, y):
    if x.time == y.time and x.event.x == y.event.x and x.event.y == y.event.y:
        return True
    return False
