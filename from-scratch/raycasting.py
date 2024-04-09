import constants as const
from map import Map
import math


class RayCasting:
    def __init__(self, player) -> None:
        # self.game = game
        self.map = Map(2)  # placeholder value
        self.player = player

    def vert_wall_distance(self, ray_angle: float) -> float:
        '''
        @ray_angle
            the angle of the sended ray (in degrees)

        @return
             the distance to the vertical intersection with a wall

        '''
        # caching repeated calculations to decrese calculation amount
        # adding a small value to the angle to avoid division by zero
        mod_ray_angle: float = ray_angle + 1e-6
        rad_angle: float = math.radians(mod_ray_angle)
        cos_a: float = math.cos(rad_angle)
        tan_a: float = math.tan(rad_angle)

        # calculating the x of first intersection and the delta_x of the following intersections
        delta_x: float
        intersect_x: int
        if 0 <= mod_ray_angle % 360 < 90 or 270 < mod_ray_angle % 360:
            delta_x = 1
            intersect_x = math.ceil(self.player.x)
        else:
            delta_x = -1
            intersect_x = math.floor(self.player.x)
        print(f"inital {intersect_x = }")

        # calculating the depth of first intersection and the delta_depth of the following intersections
        depth: float = abs(intersect_x - self.player.x) / cos_a
        print(f"inital {depth = }")
        delta_depth: float = delta_x / cos_a

        # calculating the y of first intersection and the delta_y of the following intersections
        delta_y: float = delta_x * tan_a
        intersect_y: float
        if 0 <= mod_ray_angle % 360 < 180:
            intersect_y = self.player.y + tan_a * intersect_x
        else:
            intersect_y = self.player.y - tan_a * intersect_x
        print(f"inital {intersect_y = }")

        # sending the ray deeper until collision accures, or exiting the bounds
        while depth < const.MAX_RAY_DEPTH:
            intersect_x += delta_x
            intersect_y += delta_y
            depth += delta_depth
            print(f"(vert)  {intersect_x = }, {intersect_y = }, {depth = }\n")
            if (intersect_y, intersect_x) not in self.map.get_wall_positoins():
                break

        return depth

    def hor_wall_distance(self, ray_angle: float) -> float:
        '''
        @ray_angle
            the angle of the sended ray (in degrees)

        @return
             the distance to the horizontal intersection with a wall

        '''
        # caching repeated calculations to decrese calculation amount
        # adding a small value to the angle to avoid division by zero
        mod_ray_angle: float = ray_angle + 1e-6
        rad_angle: float = math.radians(mod_ray_angle)
        sin_a: float = math.sin(rad_angle)
        tan_a: float = math.tan(rad_angle)

        # calculating the y of first intersection and the delta_y of the following intersections
        delta_y: float
        intersect_y: int
        if 0 <= mod_ray_angle % 360 < 180:
            delta_y = 1
            intersect_y = math.ceil(self.player.y)
        else:
            delta_y = -1
            intersect_y = math.floor(self.player.y)
        print(f"initial {intersect_y = }")

        # calculating the depth of first intersection and the delta_depth of the following intersections
        depth: float = abs(intersect_y - self.player.y) / sin_a
        print(f"inital {depth = }")
        delta_depth: float = delta_y / sin_a
        delta_x: float = delta_y / tan_a

        # calculating the x of first intersection and the delta_x of the following intersections
        intersect_x: float
        if 0 <= mod_ray_angle % 360 < 90 or 270 < mod_ray_angle % 360:
            intersect_x = self.player.x + intersect_y / tan_a
        else:
            intersect_x = self.player.x - intersect_y / tan_a
        print(f"inital {intersect_x = }")

        # sending the ray deeper until collision accures, or exiting the bounds
        while depth < const.MAX_RAY_DEPTH:
            intersect_x += delta_x
            intersect_y += delta_y
            depth += delta_depth
            print(f"(hor)  {intersect_x = }, {intersect_y = }, {depth = }\n")
            if (intersect_y, intersect_x) not in self.map.get_wall_positoins():
                break

        return depth
