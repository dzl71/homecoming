import constants as const
import pygame as pg


class Options:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.displaying_map: bool = False
        self.time_left: int = const.GAME_TIME
        self.rescued_hostages: int = 0
        self.map_usages: int = 300

    def display_data(self) -> None:
        font = pg.font.SysFont(const.FONT, const.FONT_SIZE)
        options = [
            font.render(
                f'Hostages rescued: {self.rescued_hostages}',
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
            )
        ]
        for idx, option in enumerate(options):
            self.screen.blit(option, (0, idx * const.FONT_SIZE))
