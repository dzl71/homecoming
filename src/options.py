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
            f'Hostages to rescue: {self.hostages_to_rescue}',
            f'Time left: {self.time_left // 60}:{self.time_left % 60:0>2}',
            f'Map usages: {self.map_usages}',
            f'PathFinding usages: {self.pathfinding_usages}',
        ]
        for idx, option_text in enumerate(options):
            self.screen.blit(
                font.render(
                    option_text,
                    False,
                    (255, 255, 255)
                ),
                (3, 3 + idx * const.FONT_SIZE)
            )

# comment to commit
