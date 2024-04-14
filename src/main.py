import sys
import time
# import multiprocessing as mp
# import classes
from object_renderer import ObjectRenderer
from raycasting import RayCasting
from player import Player
from map import Map
# import modules
import constants as const
import pygame as pg


class Game:
    def __init__(self) -> None:
        pg.init()
        pg.font.init()
        self.screen: pg.surface.Surface = pg.display.set_mode(const.RESOLUTION)
        self.clock: pg.time.Clock = pg.time.Clock()
        self.delta_time: int = 1
        self.raycast: bool = True
        self.displaying_map: bool = False
        self.time_left: int = const.GAME_TIME
        self.rescued_hostages: int = 0
        self.new_game()

    def display_data(self) -> None:
        my_font = pg.font.SysFont(const.FONT, const.FONT_SIZE)
        hostages_data = my_font.render(
            f'Hostages rescued: {self.rescued_hostages}',
            False,
            (255, 255, 255)
        )
        time_left = my_font.render(
            f'Hostages rescued: {self.time_left // 60}:{self.time_left % 60:0>2}',
            False,
            (255, 255, 255)
        )
        self.screen.blit(hostages_data, (0, 0))
        self.screen.blit(time_left, (0, const.FONT_SIZE))

    def new_game(self) -> None:
        self.map: Map = Map(self.screen)
        self.player: Player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting: RayCasting = RayCasting(self)

    def update(self) -> None:
        self.player.update()
        if self.raycast:
            self.raycasting.ray_cast(self.screen)
        self.delta_time = self.clock.tick(const.FPS)
        pg.display.set_caption(f"{self.clock.get_fps() :.1f}")

    def draw_map(self) -> None:
        self.map.draw()
        self.player.draw()

    def check_events(self) -> None:
        for event in pg.event.get():
            if event.type in (pg.QUIT, pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self) -> None:
        timer = time.time()
        while True:
            self.screen.fill('black')
            self.check_events()
            self.update()
            if self.displaying_map:
                self.draw_map()
            self.display_data()
            pg.display.flip()
            if time.time() - timer >= 1 and self.raycast:
                self.time_left -= 1
                timer = time.time()
            if self.time_left <= 0:
                break


if __name__ == '__main__':
    game = Game()
    game.run()
