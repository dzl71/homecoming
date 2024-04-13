import time
import math
import pygame as pg
import constants as const


class Player:
    def __init__(self, game) -> None:
        self.game = game
        self.angle = const.STARTING_ANGLE
        self.x = const.STARTING_X
        self.y = const.STARTING_Y

    def movement(self) -> None:
        sin_a: float = math.sin(self.angle)
        cos_a: float = math.cos(self.angle)
        speed = const.PLAYER_MOVEMENT_SPEED * self.game.delta_time
        dx: float = 0
        dy: float = 0
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx -= speed_cos
            dy -= speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy -= speed_cos
        if keys[pg.K_d]:
            dx -= speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)

        if keys[pg.K_m]:
            if not self.game.displaying_map:
                self.game.raycast = False
            else:
                self.game.raycast = True
            self.game.displaying_map = not self.game.displaying_map
            time.sleep(0.08)

        if keys[pg.K_LEFT]:
            self.angle -= const.PLAYER_ROTATION_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += const.PLAYER_ROTATION_SPEED * self.game.delta_time

        self.angle %= math.tau

    def check_wall(self, x: int, y: int) -> bool:
        return (y, x) not in self.game.map.wall_positions

    def check_wall_collision(self, dx: float, dy: float) -> None:
        scale = const.PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    # test funtion
    def draw(self) -> None:
        pg.draw.line(
            self.game.screen,
            'yellow',
            (self.x * 100, self.y * 100),
            (
                self.x * 100 + const.WIDTH * math.cos(self.angle),
                self.y * 100 + const.WIDTH * math.sin(self.angle)
            ),
            2,
        )
        # draw field of view
        # for i in range(1, const.RAY_NUM // 2 + 1):
        #     pg.draw.line(
        #         self.game.screen,
        #         'darkgray',
        #         (self.x * 100, self.y * 100),
        #         (
        #             self.x * 100 + const.WIDTH *
        #             math.cos(self.angle + const.DELTA_ANGLE * i),
        #             self.y * 100 + const.WIDTH *
        #             math.sin(self.angle + const.DELTA_ANGLE * i)
        #         ),
        #         2,
        #     )
        #     pg.draw.line(
        #         self.game.screen,
        #         'darkgray',
        #         (self.x * 100, self.y * 100),
        #         (
        #             self.x * 100 + const.WIDTH *
        #             math.cos(self.angle - const.DELTA_ANGLE * i),
        #             self.y * 100 + const.WIDTH *
        #             math.sin(self.angle - const.DELTA_ANGLE * i),
        #         ),
        #         2,
        #     )
        pg.draw.circle(
            self.game.screen,
            'green',
            (self.x * 100, self.y * 100),
            15,
        )

    def update(self) -> None:
        self.movement()
