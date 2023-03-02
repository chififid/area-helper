from collections import namedtuple

from shapely import MultiPoint
from shapely.geometry import Point
from shapely.geometry import LineString

from src.core.movements import Movement
from src.core.math_utils import get_distance, Vec2, step_to_direction_point, get_speed

PathItem = namedtuple("PathItem", "time speed pos")


def line_approximate_movements(movements, rounding_radius):
    if len(movements) < 2:
        return None

    point = movements[0]
    path = [PathItem(point.time, 0, Vec2(point.x, point.y))]

    i = 1
    while i < len(movements):
        (chain, i) = get_movements_chain_in_radius(point, rounding_radius, movements, i)

        if chain:
            last_movement = movements[i - 1]
        else:
            last_movement = point

        if i < len(movements) and rounding_radius / abs(get_distance(point, last_movement) - rounding_radius) < 10:
            next_movement = movements[i]

            g_point = Point(point.x, point.y)
            g_circle = g_point.buffer(rounding_radius).boundary

            g_line = LineString([(last_movement.x, last_movement.y), (next_movement.x, next_movement.y)])

            g_intersection = g_circle.intersection(g_line)
            if type(g_intersection) == MultiPoint:
                min_distance = None
                for i_point in g_intersection.geoms:
                    distance = get_distance(next_movement, i_point)
                    if not min_distance or distance > min_distance:
                        g_intersection = i_point

            delta_dist = get_distance(last_movement, g_intersection)
            full_dist = get_distance(last_movement, next_movement)
            delta_time = next_movement.time - last_movement.time
            new_time = last_movement.time + delta_time * (delta_dist / full_dist)

            chain.append(Movement(
                new_time,
                g_intersection.x,
                g_intersection.y,
            ))

        sum_x = sum_y = 0
        for movement in chain:
            sum_x += movement.x
            sum_y += movement.y

        direction_point = Vec2(sum_x / len(chain), sum_y / len(chain))
        new_pos = step_to_direction_point(point, direction_point, rounding_radius)
        new_point = Movement(chain[-1].time, new_pos.x, new_pos.y)

        g_line = LineString([(point.x, point.y), (new_point.x, new_point.y)])
        for movement in chain:
            dist_to_start_point = g_line.project(Point(movement.x, movement.y))
            projected_point = step_to_direction_point(point, new_point, dist_to_start_point)

            speed = get_speed(projected_point, path[-1].pos, movement.time, path[-1].time)
            if not speed:
                continue

            path.append(PathItem(movement.time, speed, Vec2(projected_point.x, projected_point.y)))

        point = Movement(path[-1].time, path[-1].pos.x, path[-1].pos.y)
    return path


def get_max_speed_on_path(path):
    return max([i.speed for i in path])


def round_points_in_path(path):
    return [Vec2(round(p.pos.x), round(p.pos.y)) for p in path]


def get_movements_chain_in_radius(point, radius, movements, last_i):
    chain = []
    i = last_i
    while i < len(movements) and get_distance(point, movements[i]) < radius:
        chain.append(movements[i])
        i += 1
    return chain, i
