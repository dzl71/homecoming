import constants as const
import pygame as pg


class Map:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.map = const.MAP
        self.wall_positions = self.get_wall_positoins()
        self.marked_positions = self.get_marked_positions()

    def get_wall_positoins(self) -> dict[tuple[int, int], int]:
        wall_positoins: dict[tuple[int, int], int] = {}
        for row_idx, row in enumerate(self.map):
            for tile_idx, tile in enumerate(row):
                if tile > 0:
                    wall_positoins[(row_idx, tile_idx)] = tile
        return wall_positoins

    def get_marked_positions(self) -> set[tuple[int, int]]:
        marked_positoins: set[tuple[int, int]] = set()
        for row_idx, row in enumerate(self.map):
            for tile_idx, tile in enumerate(row):
                if tile == -1:
                    marked_positoins.add((row_idx, tile_idx))
        return marked_positoins

    def draw(self) -> None:
        for pos in self.wall_positions:
            self.screen.fill(
                'darkgray',
                (pos[1] * 100, pos[0] * 100, 100, 100),
            )
        for pos in self.marked_positions:
            self.screen.fill(
                'red',
                (pos[1] * 100, pos[0] * 100, 100, 100),
            )
