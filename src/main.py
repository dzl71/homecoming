import sys
import random
import time
# from Maze_Gen_Sol import in_use
# import multiprocessing as mp
# import classes
from pathfinding import PathFinding
from object_renderer import ObjectRenderer
from options import Options
from raycasting import RayCasting
from player import Player
from music import Music
from map import Map
# import modules
import constants as const
import pygame as pg

# sys.path.insert(0, "./SearchAlgo")


class Game:
    def __init__(self) -> None:
        # in_use()
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
        self.searched_hostage = random.choice(list(self.map.hostages))
        self.pathfinding_tile = None

    def update(self) -> None:
        self.player.movement()
        pg.mouse.set_pos(const.HALF_WIDTH, const.HALF_HEIGHT)
        if not self.options.displaying_map:
            self.raycasting.raycast()
        self.delta_time = self.clock.tick(const.FPS)
        pg.display.set_caption(f"{self.clock.get_fps() :.1f}")
        if self.map.marked:
            self.show_path_to_hostage()

    def show_path_to_hostage(self) -> None:
        self.pathfinding_tile = self.pathfinding.get_path(
            self.pathfinding_tile,
            self.searched_hostage,
        )
        # print(f"{self.pathfinding_tile = }")
        self.map.marked.add(self.pathfinding_tile)

    def stop_conditions_met(self) -> bool:
        return (
            self.options.time_left <= 0
            or self.options.hostages_to_rescue <= 0
        )

    def run(self) -> None:
        timer = time.time()
        while True:
            self.screen.fill('black')
            check_quit_events()
            self.update()
            if self.options.displaying_map:
                self.map.draw_map()
            self.options.display_data()

            pg.display.flip()

            # timer
            if time.time() - timer >= 1 and not self.options.displaying_map:
                self.options.time_left -= 1
                timer = time.time()

            if self.stop_conditions_met():
                break

    def opening_screen(self, sleep_time):
        t = time.time()
        while time.time() - t < sleep_time:
            self.screen.blit(
                self.object_renderer.get_texture(
                    f"{const.MENU_IMG_PATH}/BRING_THEM_HOME_NOW_open.jpg",
                    const.RESOLUTION,
                ),
                (0, 0)
            )
            pg.display.flip()

    def end_screen(self):
        # stop music
        # blure the background
        self.object_renderer.path_extention = "blurred/"
        self.object_renderer.set_textures()
        self.raycasting.raycast()
        if self.options.hostages_to_rescue <= 0:
            # self.music.play_vicory()
            main_text = const.SUCCESS_MAIN_MESSAGE
            sub_text = const.SUCCESS_SUB_MESSAGE
        else:
            # self.music.p
            main_text = const.FAIL_MAIN_MESSAGE
            sub_text = const.FAIL_SUB_MESSAGE
        # main text
        font_pos = (100, 200)
        font_size = const.FONT_SIZE * 4
        font = pg.font.SysFont(const.FONT, font_size)
        self.screen.blit(
            font.render(
                main_text,
                False,
                (255, 255, 255),
            ),
            font_pos
        )
        # sub text
        font_pos = (font_pos[0] + 100, font_pos[1] + font_size)
        font = pg.font.SysFont(const.FONT, const.FONT_SIZE * 3)
        self.screen.blit(
            font.render(
                sub_text,
                False,
                (255, 255, 255),
            ),
            font_pos
        )
        font = pg.font.SysFont(const.FONT, const.FONT_SIZE)
        self.screen.blit(
            font.render(
                "hold space key to return to menu",
                False,
                (255, 255, 255),
            ),
            (
                const.WIDTH / 2 - 300, const.HEIGHT -
                const.FONT_SIZE / 2 - 45 - const.FONT_SIZE
            )
        )
        self.screen.blit(
            font.render(
                "hold esc key to exit game",
                False,
                (255, 255, 255),
            ),
            (const.WIDTH / 2 - 250, const.HEIGHT - const.FONT_SIZE / 2 - 40)
        )

        pg.display.flip()

    def display_menu(self):
        self.screen.blit(
            self.object_renderer.get_texture(
                f"{const.MENU_IMG_PATH}/BRING_THEM_HOME_NOW_menu.png",
                const.RESOLUTION
            ),
            (0, 0)
        )
        font = pg.font.SysFont(const.FONT, const.FONT_SIZE * 2)
        for idx, string in enumerate([
            "- press space to start game",
            "- press escape to quit game",
        ]):
            self.screen.blit(
                font.render(
                    string,
                    False,
                    (255, 255, 255)
                ),
                (const.HALF_WIDTH - 500, const.HEIGHT / 1.5 + const.HEIGHT / 8 * idx)
            )
        while True:
            pg.display.flip()
            key = pg.key.get_pressed()
            if key[pg.K_SPACE]:
                break
            check_quit_events()

    def display_tutorial(self) -> None:
        self.screen.fill("black", (0, 0, const.WIDTH, const.HEIGHT))
        font = pg.font.SysFont(const.FONT, const.FONT_SIZE)
        self.screen.blit(
            font.render(
                "press any key to continue",
                False,
                (255, 255, 255),
            ),
            (const.WIDTH / 2 - 250, const.HEIGHT - const.FONT_SIZE / 2 - 40)
        )
        font = pg.font.SysFont(const.FONT, const.FONT_SIZE * 3)
        self.screen.blit(
            font.render(
                'Controls',
                False,
                (255, 255, 255),
            ),
            (const.WIDTH / 2 - 150, const.HEIGHT / 10)
        )
        messages = [
            '- W/A/S/D to move forward/left/backwards/right respectively',
            '- use the mouse or the "<-" "->" keys to rotate the camera',
            '- press the "v" key to [v]iew the map',
            '- press the "f" key to [f]ind the the closest path to a hostage',
            '- you will see in the top left angle of the screen additional info',
            '- press the escape key to exit the game',
        ]
        font = pg.font.SysFont(const.FONT, const.FONT_SIZE * 1)
        for i, message in enumerate(messages):
            self.screen.blit(
                font.render(
                    message,
                    False,
                    (255, 255, 255),
                ),
                (const.WIDTH / 10, const.HEIGHT / 10 + const.HEIGHT / 8 * (i + 1))
            )
        waiting = True
        while waiting:
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    return None


def check_quit_events() -> None:
    for event in pg.event.get():
        if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
            pg.quit()
            sys.exit()


if __name__ == '__main__':
    game = Game()
    music: Music = Music()
    music.play_music()
    while True:
        music.rewind_music()

        game.opening_screen(3)
        game.display_menu()
        game.display_tutorial()
        game.run()
        while not pg.key.get_pressed()[pg.K_SPACE]:
            check_quit_events()
            game.end_screen()

        # reset the game parameters
        game.new_game()


# comment to commit
