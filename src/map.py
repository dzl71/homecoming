import pygame as pg
import constants as const


class Map:
    def __init__(self, screen: pg.Surface) -> None:
        self.game_screen: pg.Surface = screen
        self.mini_map: list[list[int]] = const.MAP
        self.world_map: dict[tuple[int, int], int] = {}
        self.get_map()

    def get_map(self) -> None:
        for row_idx, row in enumerate(self.mini_map):
            for tile_idx, tile in enumerate(row):
                if tile:
                    self.world_map[(tile_idx, row_idx)] = tile

    # test method
    def draw(self) -> None:
        [
            pg.draw.rect(
                self.game_screen,
                'darkgray',
                (pos[0] * 100, pos[1] * 100, 100, 100),
                2,
            )
            for pos in self.world_map
        ]
