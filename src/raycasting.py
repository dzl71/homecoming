import constants as const
import math
import pygame as pg


class RayCasting:
    def __init__(self, game) -> None:
        self.game = game

    def ray_cast(self) -> None:
        player_x: float
        player_y: float
        (player_x, player_y) = self.game.player.pos()
        map_x: float
        map_y: float
        (map_x, map_y) = self.game.player.map_pos()

        ray_angle = self.game.player.angle - const.HALF_FOV + 0.0001
        for ray in range(const.RAYS_NUM):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)
            ray_angle + const.DELTA_ANGLE

    def update(self) -> None:
        pass
