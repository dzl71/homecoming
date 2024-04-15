import math
import constants as const
from map import Map
from player import Player


def pos_cos(angle: float) -> bool:
    return (
        0 <= angle % math.tau < math.pi / 2 or math.pi * 1.5 < angle % math.tau
    )


def pos_sin(angle: float) -> bool:
    return 0 < angle % math.tau < math.pi


class RayCasting:
    def __init__(self, game) -> None:
        # self.game = game
        self.map: Map = game.map  # placeholder value
        self.player: Player = game.player
        self.object_renderer = game.object_renderer

    def vert_wall_distance(self, ray_angle: float) -> tuple[float, int, float]:
        '''
        @ray_angle
            the angle of the sended ray (in radians)

        @return
             tuple(
                 the distance to the vertical intersection with a wall,
                 the enumeration of the wall texture,
                 y value of the intersection
             )

        '''
        # caching repeated calculations to decrese calculation amount
        # adding a small value to the angle to avoid division by zero
        ray_angle += 1e-6
        cos_a: float = math.cos(ray_angle)
        sin_a: float = math.sin(ray_angle)

        # calculating the x of first intersection and the delta_x of the following intersections
        intersect_x: int
        delta_x: float
        if pos_cos(ray_angle):
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

        # sending the ray deeper until collision accures, or exiting the bounds
        texture: int = self.object_renderer.default_texture
        for _ in range(const.MAX_RAY_DEPTH):
            tile: tuple[int, int] = (int(intersect_x), int(intersect_y))
            if tile in self.map.wall_positions:
                texture = self.map.wall_positions[tile]
                break
            intersect_x += delta_x
            intersect_y += delta_y
            depth += delta_depth

        return (depth, texture, intersect_y)

    def hor_wall_distance(self, ray_angle: float) -> tuple[float, int, float]:
        '''
        @ray_angle
            the angle of the sended ray (in radians)

        @return
             tuple(
                the distance to the horizontal intersection with a wall,
                the enumeration of the wall texture,
                x value of the intersection
             )

        '''
        # caching repeated calculations to decrese calculation amount
        # adding a small value to the angle to avoid division by zero
        ray_angle += 1e-6
        sin_a: float = math.sin(ray_angle)
        cos_a: float = math.cos(ray_angle)

        # calculating the y of first intersection and the delta_y of the following intersections
        delta_y: float
        intersect_y: int
        if pos_sin(ray_angle):
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

        # sending the ray deeper until collision accures, or exiting the bounds
        texture: int = self.object_renderer.default_texture
        for _ in range(const.MAX_RAY_DEPTH):
            tile: tuple[int, int] = (int(intersect_x), int(intersect_y))
            if tile in self.map.wall_positions:
                texture = self.map.wall_positions[tile]
                break
            intersect_x += delta_x
            intersect_y += delta_y
            depth += delta_depth

        return (depth, texture, intersect_x)

    def ray_cast(self, screen) -> None:
        ray_angle: float = self.player.angle - const.HALF_FOV + 1e-6
        for ray in range(const.RAY_NUM):

            vert_depth: float
            vert_texture: int
            vert_y: float
            (vert_depth, vert_texture, vert_y) = self.vert_wall_distance(ray_angle)
            hor_depth: float
            hor_texture: int
            hor_x: float
            (hor_depth, hor_texture, hor_x) = self.hor_wall_distance(ray_angle)

            ray_depth: float
            offset: float
            texture: int
            if vert_depth < hor_depth:
                texture = vert_texture
                ray_depth = vert_depth
                vert_y %= 1
                offset = vert_y if pos_cos(ray_angle) else 1 - vert_y
            else:
                texture = hor_texture
                ray_depth = hor_depth
                hor_x %= 1
                offset = hor_x if not pos_sin(ray_angle) else 1 - hor_x

            # remove the fishblow effect
            ray_depth *= math.cos(self.player.angle - ray_angle)

            # projection height
            proj_height = const.SCREEN_DISTANCE / (ray_depth + 1e-6)

            self.object_renderer.render_floor_ceil_column(
                screen,
                ray,
                const.HALF_HEIGHT + proj_height // 2 - 1,
                ray_angle
            )

            if ray_depth >= const.MAX_RAY_DEPTH:
                ray_angle += const.DELTA_ANGLE
                continue

            self.object_renderer.render_wall_column(
                texture,
                offset,
                proj_height,
                ray
            )

            ray_angle += const.DELTA_ANGLE
