import unittest

from src.core.math_utils import Vec2
from src.core.objects.HitObj import HitObj, HitObjType


class HitObjTest(unittest.TestCase):
    def test_parse_note_str(self):
        obj = HitObj.parse_from_str("231,260,30695,1,0,0:0:0:0:")
        expected_result_obj_dict = {
            "time": 30695,
            "obj_type": HitObjType.Circle,
            "position": Vec2(231, 260),
        }
        self.assertTrue(expected_result_obj_dict.items() <= obj.__dict__.items())

    def test_parse_slider_str(self):
        obj = HitObj.parse_from_str("74,251,30807,38,0,L|181:307,1,100,14|0,0:0|0:0,0:0:0:0:")
        expected_result_obj_dict = {
            "time": 30807,
            "obj_type": HitObjType.Slider,
            "points": [[Vec2(74, 251), Vec2(x=181, y=307)]],
            "repeat": 1,
            "length": 100.0,
        }
        print(obj.__dict__.items())
        self.assertTrue(expected_result_obj_dict.items() <= obj.__dict__.items())

    def test_change_note(self):
        obj = HitObj(200, HitObjType.Circle)
        obj.set_note_data(Vec2(100, 222))
        new_line = obj.change_osu_line("0,0,0,1,0,0:0:0:0:")
        self.assertTrue(new_line, "100,222,0,1,0,0:0:0:0:")
