import constants as const
import math
import pygame as pg


class RayCasting:
    def __init__(self, game) -> None:
        self.game = game

    def ray_cast(self) -> None:
        player_pos = self.game.player.pos()
        player_x: float = player_pos[0]
        player_y: float = player_pos[1]
        map_pos = self.game.player.map_pos()
        map_x: float = map_pos[0]
        map_y: float = map_pos[1]

        ray_angle = self.game.player.angle - const.HALF_FOV + 0.0001
        print(ray_angle)
        for ray in range(const.RAYS_NUM):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # horizontal intersections
            hor_intersect_y: int
            dy: int
            if 0 < ray_angle % math.tau < math.pi:
                (hor_intersect_y, dy) = (map_y + 1, 1)
            else:
                (hor_intersect_y, dy) = (map_y - 1e-6, -1)

            hor_intersect_depth: float = (hor_intersect_y - player_y) / sin_a
            hor_intersect_x: float = player_x + hor_intersect_depth * cos_a

            delta_depth: float = dy / sin_a
            dx: float = delta_depth * cos_a

            for _ in range(const.MAX_DEPTH):
                hor_intersect_tile: tuple[int, int] = (
                    int(hor_intersect_x), int(hor_intersect_y)
                )
                if hor_intersect_tile in self.game.map.world_map:
                    break
                hor_intersect_x += dx
                hor_intersect_y += dy
                hor_intersect_depth += delta_depth

            # vertical intersections
            vert_intersect_x: int
            dx: int
            if ray_angle % math.tau < math.pi / 2 or ray_angle % math.tau > math.pi * 1.5:
                (vert_intersect_x, dx) = (map_x + 1, 1)
            else:
                (vert_intersect_x, dx) = (map_x - 1e-6, -1)

            vert_intersect_depth: float = (vert_intersect_x - player_x) / cos_a
            vert_intersect_y: float = player_y + vert_intersect_depth * sin_a

            delta_depth: float = dx / cos_a
            dy: float = delta_depth * sin_a

            for _ in range(const.MAX_DEPTH):
                vert_intersect_tile: tuple[int, int] = (
                    int(vert_intersect_x), int(vert_intersect_y)
                )
                if vert_intersect_tile in self.game.map.world_map:
                    break
                vert_intersect_x += dx
                vert_intersect_y += dy
                vert_intersect_depth += delta_depth

            # determining the depth
            depth: float = min(vert_intersect_depth, hor_intersect_depth)

            # draw for debug
            # pg.draw.line(
            #     self.game.screen,
            #     'darkgray',
            #     (player_x * 100, player_y * 100),
            #     (
            #         player_x * 100 + 100 * depth * cos_a,
            #         player_y * 100 + 100 * depth * sin_a
            #     ),
            #     2
            # )

            # remove fishblow effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # projection height
            proj_height = const.SCREEN_DISTANCE / (depth + 1e-6)

            # draw walls
            color = [255 / (1 + depth ** 5 * 2e-5)] * 3
            pg.draw.rect(
                self.game.screen,
                'white',
                (
                    ray * const.SCALE, const.HALF_HEIGHT - proj_height // 2,
                    const.SCALE,
                    proj_height
                ),
            )

            ray_angle += const.DELTA_ANGLE

    def update(self) -> None:
        self.ray_cast()


class FloorCasting():
    pass
