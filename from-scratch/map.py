import constants as const
import pygame as pg


class Map:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.minimap = const.MAP

    def get_wall_positoins(self) -> dict[tuple[int, int], int]:
        wall_positoins: dict[tuple[int, int], int] = {}
        for row_idx, row in enumerate(self.minimap):
            for tile_idx, tile in enumerate(row):
                wall_positoins[(row_idx, tile_idx)] = tile
        return wall_positoins
