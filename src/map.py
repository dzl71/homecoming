import math
import constants as const
import pygame as pg


class Map:
    def __init__(self, game) -> None:
        self.screen = game.screen
        self.player = game.player
        self.map = const.MAP
        self.wall_positions = self.get_wall_positoins()
        self.marked_positions = self.get_marked_positions()

    def get_wall_positoins(self) -> dict[tuple[int, int], int]:
        wall_positoins: dict[tuple[int, int], int] = {}
        for row_idx, row in enumerate(self.map):
            for tile_idx, tile in enumerate(row):
                if tile > 0:
                    wall_positoins[(tile_idx, row_idx)] = tile
        return wall_positoins

    def get_marked_positions(self) -> set[tuple[int, int]]:
        marked_positoins: set[tuple[int, int]] = set()
        for row_idx, row in enumerate(self.map):
            for tile_idx, tile in enumerate(row):
                if tile == -1:
                    marked_positoins.add((tile_idx, row_idx))
        return marked_positoins

    def draw_static(self, positions, color) -> tuple[int, int]:
        origin_pos: tuple[int, int] = None
        left_bound = int(self.player.x) - const.MINIMAP_HALF_WIDTH
        right_bound = int(self.player.x) + const.MINIMAP_HALF_WIDTH
        while left_bound < 0:
            left_bound += 1
            right_bound += 1
        upper_bound = int(self.player.y) - const.MINIMAP_HALF_HEIGHT
        lower_bound = int(self.player.y) + const.MINIMAP_HALF_HEIGHT
        while upper_bound < 0:
            upper_bound += 1
            lower_bound += 1
        for pos in positions:
            if (
                left_bound <= pos[0] <= right_bound
                and
                upper_bound <= pos[1] <= lower_bound
            ):
                if origin_pos is None:
                    origin_pos = pos
                self.screen.fill(
                    color,
                    (
                        (pos[0] - origin_pos[0]) * const.MAP_SCALER,
                        (pos[1] - origin_pos[1]) * const.MAP_SCALER,
                        const.MAP_SCALER,
                        const.MAP_SCALER,
                    )
                )
        return origin_pos

    def draw_player(self, pos_x: float, pos_y: float) -> None:
        pg.draw.circle(
            self.screen,
            'green',
            (pos_x, pos_y),
            15,
        )

    def draw_map(self) -> None:
        origin_pos = self.draw_static(self.wall_positions, 'darkgray')
        self.draw_static(self.marked_positions, 'red')
        self.draw_player(
            (self.player.x - origin_pos[0]) * const.MAP_SCALER,
            (self.player.y - origin_pos[1]) * const.MAP_SCALER
        )
