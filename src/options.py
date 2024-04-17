import constants as const
import pygame as pg


class Options:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.displaying_map: bool = False
        self.time_left: int = const.GAME_TIME
        self.hostages_to_rescue: int = const.HOSTAGES_PLACED
        self.map_usages: int = 3
        self.pathfinding_usages: int = 1

    def display_data(self) -> None:
        font = pg.font.SysFont(const.FONT, const.FONT_SIZE)
        options = [
            font.render(
                f'Hostages to rescue: {self.hostages_to_rescue}',
                False,
                (255, 255, 255)
            ),
            font.render(
                f'Time left: {self.time_left // 60}:{self.time_left % 60:0>2}',
                False,
                (255, 255, 255)
            ),
            font.render(
                f'Map usages: {self.map_usages}',
                False,
                (255, 255, 255)
            ),
            font.render(
                f'PathFinding usages: {self.pathfinding_usages}',
                False,
                (255, 255, 255)
            ),
        ]
        for idx, option in enumerate(options):
            self.screen.blit(option, (0, idx * const.FONT_SIZE))

# comment to commit