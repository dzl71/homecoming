import sys
import time
# import multiprocessing as mp
# import classes
from pathfinding import PathFinding
from object_renderer import ObjectRenderer
from options import Options
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
        self.new_game()

    def new_game(self) -> None:
        pg.mouse.set_pos(const.HALF_WIDTH, const.HALF_HEIGHT)
        pg.mouse.set_visible(False)
        self.player: Player = Player(self)
        self.map: Map = Map(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting: RayCasting = RayCasting(self)
        self.options: Options = Options(self.screen)
        self.pathfinding: PathFinding = PathFinding(self)
        self.next_tile = self.pathfinding.get_path((2, 1), (7, 8))

    def update(self) -> None:
        self.player.movement()
        pg.mouse.set_pos(const.HALF_WIDTH, const.HALF_HEIGHT)
        if not self.options.displaying_map:
            self.raycasting.raycast()
        self.delta_time = self.clock.tick(const.FPS)
        pg.display.set_caption(f"{self.clock.get_fps() :.1f}")
        self.next_tile = self.pathfinding.get_path(self.next_tile, (7, 8))
        self.map.marked.add(self.next_tile)
        print(f"{self.next_tile = }")
        print(f"{self.map.map = }")

    def check_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def run(self) -> None:
        timer = time.time()
        while True:
            self.screen.fill('black')
            self.check_events()
            self.update()
            if self.options.displaying_map:
                self.map.draw_map()
            self.options.display_data()

            pg.display.flip()

            if time.time() - timer >= 1 and not self.options.displaying_map:
                self.options.time_left -= 1
                timer = time.time()
            if self.options.time_left <= 0:
                break


if __name__ == '__main__':
    game = Game()
    game.run()
