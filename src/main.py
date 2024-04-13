import sys
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
        self.screen: pg.surface.Surface = pg.display.set_mode(const.RESOLUTION)
        self.clock: pg.time.Clock = pg.time.Clock()
        self.delta_time: int = 60
        self.object_renderer = ObjectRenderer(self.screen)
        self.raycast: bool = True
        self.displaying_map: bool = False
        self.new_game()

    def new_game(self) -> None:
        self.map: Map = Map(self.screen)
        self.player: Player = Player(self)
        self.raycasting: RayCasting = RayCasting(self)

    def update(self) -> None:
        self.player.update()
        if self.raycast == True:
            self.raycasting.ray_cast(self.screen)
        pg.display.flip()
        self.delta_time = self.clock.tick(const.FPS)
        pg.display.set_caption(f"{self.clock.get_fps() :.1f}")

    def draw(self) -> None:
        self.screen.fill('black')
        self.map.draw()
        self.player.draw()

    def check_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.K_ESCAPE:
                pg.quit()
                sys.exit()

    def run(self) -> None:
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
