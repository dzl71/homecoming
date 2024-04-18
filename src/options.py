import constants as const
import pygame as pg


class Options:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.displaying_map: bool = False
        self.crit_time = False
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
                const.REGULAR_COLOR
            ),
            font.render(
                f'Time left: {self.time_left // 60}:{self.time_left % 60:0>2}',
                False,
                const.REGULAR_COLOR if self.time_left > 30 else const.CRIT_COLOR
            ),
            font.render(
                f'Map usages: {self.map_usages}',
                False,
                const.REGULAR_COLOR if self.map_usages > 0 else const.CRIT_COLOR
            ),
            font.render(
                f'Path finding usages: {self.pathfinding_usages}',
                False,
                const.REGULAR_COLOR if self.pathfinding_usages > 0 else const.CRIT_COLOR
            ),
        ]
        for idx, option in enumerate(options):
            self.screen.blit(
                option,
                (3, 3 + idx * const.FONT_SIZE)
            )

# comment to commit
