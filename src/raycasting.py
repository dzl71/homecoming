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
        self.game = game
        self.screen = game.screen
        self.map: Map = game.map  # placeholder value
        self.player: Player = game.player
        self.object_renderer = game.object_renderer

    def vert_intersect_for(self, ray_angle: float, object_positions, default_texture) -> tuple[float, int, float]:
        '''
        @ray_angle
            the angle of the sended ray (in radians)

        @return
             tuple(
                 the depth to the vertical intersection,
                 the enumeration of the texture,
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
        texture: int = default_texture
        for _ in range(const.MAX_RAY_DEPTH):
            tile: tuple[int, int] = (int(intersect_x), int(intersect_y))
            if tile in object_positions:
                texture = object_positions[tile]
                break
            intersect_x += delta_x
            intersect_y += delta_y
            depth += delta_depth

        return (depth, texture, intersect_y)

    def hor_intersect_for(self, ray_angle: float, object_positions, default_texture) -> tuple[float, int, float]:
        '''
        @ray_angle
            the angle of the sended ray (in radians)

        @return
             tuple(
                 the depth to the horizontal intersection,
                 the enumeration of the texture,
                 x value of the intersection
             )

        '''
        # caching repeated calculations to decrese calculation amount
        # adding a small value to the angle to avoid division by zero
        ray_angle += 1e-6
        sin_a: float = math.sin(ray_angle)
        cos_a: float = math.cos(ray_angle)

        # calculating the y of first intersection and the delta_y of the following intersections
        intersect_y: int
        delta_y: float
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
        texture: int = default_texture
        for _ in range(const.MAX_RAY_DEPTH):
            tile: tuple[int, int] = (int(intersect_x), int(intersect_y))
            if tile in object_positions:
                texture = object_positions[tile]
                break
            intersect_x += delta_x
            intersect_y += delta_y
            depth += delta_depth

        return (depth, texture, intersect_x)

    def get_closest(self, ray_angle, objet_positions, default_texture) -> None:
        sin_a: float = math.sin(ray_angle)
        cos_a: float = math.cos(ray_angle)

        vert = self.vert_intersect_for(
            ray_angle, objet_positions, default_texture
        )
        hor = self.hor_intersect_for(
            ray_angle, objet_positions, default_texture
        )

        res = min(vert, hor, key=lambda t: t[0])

        depth = res[0]
        texture = res[1]
        temp_offet = res[2] % 1

        if res == vert:
            offset = temp_offet if cos_a > 0 else (1 - temp_offet)
        else:
            offset = (1 - temp_offet) if sin_a > 0 else temp_offet

        # remove the fishblow effect
        depth *= math.cos(self.player.angle - ray_angle)

        return (depth, offset, texture)

    def raycast(self) -> None:
        ray_angle: float = self.player.angle - const.HALF_FOV + 1e-6
        for ray in range(const.RAY_NUM):

            (wall_depth, wall_offset, wall_texture) = self.get_closest(
                ray_angle, self.map.walls, 1
            )

            (hostage_depth, hostage_offset, hostage_texture) = self.get_closest(
                ray_angle, self.map.hostages, -1
            )

            # projection height
            wall_proj_height = const.SCREEN_DISTANCE / (wall_depth + 1e-6)
            hostage_proj_height = const.SCREEN_DISTANCE / (hostage_depth + 1e-6)

            self.object_renderer.render_floor_ceil_column(
                ray,
                const.HALF_HEIGHT + wall_proj_height // 2 - 1,
                ray_angle
            )

            if wall_depth >= const.MAX_RAY_DEPTH:
                ray_angle += const.DELTA_ANGLE
                continue

            self.object_renderer.render_texture_column(
                wall_texture,
                wall_offset,
                wall_proj_height,
                ray,
                (const.TEXTURE_SIZE, const.TEXTURE_SIZE),
            )

            if hostage_depth < wall_depth:
                self.object_renderer.render_texture_column(
                    hostage_texture,
                    hostage_offset,
                    hostage_proj_height,
                    ray,
                    (const.TEXTURE_SIZE, const.TEXTURE_SIZE),
                )

            ray_angle += const.DELTA_ANGLE
