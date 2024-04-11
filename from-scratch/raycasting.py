import math
import pygame as pg
import constants as const
from map import Map


class RayCasting:
    def __init__(self, game) -> None:
        # self.game = game
        self.map = game.map  # placeholder value
        self.player = game.player

    def vert_wall_distance(self, ray_angle: float) -> float:
        '''
        @ray_angle
            the angle of the sended ray (in degrees)

        @return
             the distance to the vertical intersection with a wall

        '''
        # caching repeated calculations to decrese calculation amount
        # adding a small value to the angle to avoid division by zero
        rad_angle: float = math.radians(ray_angle)
        cos_a: float = math.cos(rad_angle)
        sin_a: float = math.sin(rad_angle)

        # calculating the x of first intersection and the delta_x of the following intersections
        intersect_x: int
        delta_x: float
        if 0 <= ray_angle % 360 < 90 or 270 < ray_angle % 360:
            delta_x = 1
            intersect_x = math.ceil(self.player.x)
        else:
            delta_x = -1
            intersect_x = math.floor(self.player.x) - 1e-6

        # calculating the depth of first intersection and the delta_depth of the following intersections
        depth: float = (intersect_x - self.player.x) / cos_a
        delta_depth: float = delta_x / cos_a

        # calculating the y of first intersection and the delta_y of the following intersections
        delta_y: float = delta_depth * sin_a
        intersect_y: float = self.player.y + depth * sin_a

        if ray_angle == self.player.angle - const.HALF_FOV + 1e-6:
            print(f"initial_vert_{intersect_x = }, initial_vert_{intersect_y = }")

        # sending the ray deeper until collision accures, or exiting the bounds
        for _ in range(const.MAX_RAY_DEPTH):
            if (int(intersect_y), int(intersect_x)) in self.map.wall_positions:
                break
            intersect_x += delta_x
            intersect_y += delta_y
            depth += delta_depth

        if ray_angle == self.player.angle - const.HALF_FOV + 1e-6:
            print(f"vert_{intersect_x = }, vert_{intersect_y = }\n")

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
        rad_angle: float = math.radians(ray_angle)
        sin_a: float = math.sin(rad_angle)
        cos_a: float = math.cos(rad_angle)

        # calculating the y of first intersection and the delta_y of the following intersections
        delta_y: float
        intersect_y: int
        if 0 < ray_angle % 360 < 180:
            delta_y = 1
            intersect_y = math.ceil(self.player.y)
        else:
            delta_y = -1
            intersect_y = math.floor(self.player.y) - 1e-6

        # calculating the depth of first intersection and the delta_depth of the following intersections
        depth: float = (intersect_y - self.player.y) / sin_a
        delta_depth: float = delta_y / sin_a

        # calculating the x of first intersection and the delta_x of the following intersections
        delta_x: float = delta_depth * cos_a
        intersect_x: float = self.player.x + depth * cos_a

        if ray_angle == self.player.angle - const.HALF_FOV + 1e-6:
            print(f"initial_hor_{intersect_x = }, initial_hor_{intersect_y = }")

        # sending the ray deeper until collision accures, or exiting the bounds
        for _ in range(const.MAX_RAY_DEPTH):
            if (int(intersect_y), int(intersect_x)) in self.map.wall_positions:
                break
            intersect_x += delta_x
            intersect_y += delta_y
            depth += delta_depth

        if ray_angle == self.player.angle - const.HALF_FOV + 1e-6:
            print(f"hor_{intersect_x = }, hor_{intersect_y = }\n")

        return depth

    def ray_cast(self, screen) -> None:
        ray_angle: float = self.player.angle - const.HALF_FOV + 1e-6
        for ray in range(const.RAY_NUM):
            ray_depth: float = min(
                self.vert_wall_distance(ray_angle),
                self.hor_wall_distance(ray_angle)
            )
            if ray_angle == self.player.angle - const.HALF_FOV + 1e-6:
                print(f"{math.radians(ray_angle) = }")
                print(f"{self.vert_wall_distance(ray_angle) = }")
                print(f"{self.hor_wall_distance(ray_angle) = }")
                print(f"{ray_depth = }")
                print("\n====================================================\n")

            # remove the fishblow effect
            ray_depth *= math.cos(math.radians(self.player.angle - ray_angle))

            # projection height
            proj_height = const.SCREEN_DISTANCE / (ray_depth + 1e-6)

            # draw walls
            # color = [255 / (1 + depth ** 5 * 2e-5)] * 3
            pg.draw.rect(
                screen,
                'white',
                (
                    ray * const.SCALE,
                    const.HALF_HEIGHT - proj_height // 2,
                    const.SCALE,
                    proj_height
                ),
            )

            ray_angle += const.DELTA_ANGLE
