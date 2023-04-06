import re
from enum import IntFlag

from matplotlib import pyplot as plt

from src.core.math_utils import Vec2


class HitObj:
    def __init__(self, time, obj_type):
        self.time = time
        self.obj_type = obj_type

        # Note inf
        self.position = None

        # Slider inf
        self.points = None
        self.repeat = None
        self.length = None

    @staticmethod
    def parse_from_str(hit_obj_str):
        data = hit_obj_str.split(",")

        time = int(data[2])  # Ms
        obj_type = int(data[3])

        if HitObjType.Circle & obj_type:
            hit_obj = HitObj(time, HitObjType.Circle)
            hit_obj.parse_note_data(hit_obj_str)
            return hit_obj
        elif HitObjType.Slider & obj_type:
            hit_obj = HitObj(time, HitObjType.Slider)
            hit_obj.parse_slider_data(hit_obj_str)
            return hit_obj
        else:
            return None

    def parse_note_data(self, note_string):
        data = note_string.split(",")

        self.position = Vec2(int(data[0]), int(data[1]))

    def parse_slider_data(self, slider_string):
        sections = slider_string.split("|")

        points = [[]]
        for section in sections:
            sections_data = section.split(",")

            if ":" in sections_data[0]:
                tick_pos = sections_data[0].split(":")
                tick_pos = Vec2(int(tick_pos[0]), int(tick_pos[1]))

                if len(sections_data) > 1:
                    self.repeat = int(sections_data[1])
                    self.length = float(sections_data[2])  # Osu px
                    points[-1].append(tick_pos)
                    break
            else:  # First tick
                tick_pos = Vec2(int(sections_data[0]), int(sections_data[1]))

            if len(points[-1]) and points[-1][-1] == tick_pos:  # New section
                points.append([tick_pos])
            else:
                points[-1].append(tick_pos)

        self.points = points

    def set_note_data(self, position):
        self.position = position

    def set_slider_data(self, points, repeat, length):
        self.points = points
        self.repeat = repeat
        self.length = length

    def print_slider(self, interval=None):  # In seconds
        points = sum(self.points, [])
        for (i, p) in enumerate(points[1:], 1):
            l_p = points[i - 1]
            plt.plot([l_p.x, p.x], [-l_p.y, -p.y], marker="o", markersize=8, color="green")
            if l_p.x == p.x and l_p.y == p.y:
                plt.plot(l_p.x, -l_p.y, marker="o", markersize=15, color="red")
            if interval:
                plt.pause(interval)
        plt.show()

    def change_osu_line(self, osu_line):
        if self.obj_type == HitObjType.Circle:
            last_data = osu_line.split(",")
            return f"{round(self.position.x)},{round(self.position.y)},{','.join(last_data[2:])}"
        else:
            points = sum(self.points, [])

            last_data = osu_line.split("|", 1)
            base_data = ",".join(last_data[0].split(",")[2:])
            additional_data = re.match(r"\d+\,\d+(.*)", last_data[1].split(",", 1)[1]).groups()[0]

            new_line = f"{points[0].x},{points[0].y},{base_data}"
            for point in points:
                new_line = f"{new_line}|{point.x}:{point.y}"
            new_line = f"{new_line},{self.repeat},{self.length}"

            if additional_data:
                new_line = f"{new_line}{additional_data}"

            return new_line


class HitObjType(IntFlag):
    Circle = 1 << 0
    Slider = 1 << 1
