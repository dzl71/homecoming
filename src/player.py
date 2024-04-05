import constants as const
import pygame as pg
import math
# from main import Game


class Player:
    def __init__(self, game) -> None:
        self.game = game
        self.x: float = const.PLAYER_POS[0]
        self.y: float = const.PLAYER_POS[1]
        self.angle: float = const.PLAYER_ANGLE

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

        if keys[pg.K_LEFT]:
            self.angle -= const.PLAYER_ROTATION_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += const.PLAYER_ROTATION_SPEED * self.game.delta_time

        self.angle %= math.tau

    def check_wall(self, x: int, y: int) -> bool:
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx: float, dy: float) -> None:
        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy)):
            self.y += dy

    # test funtion
    def draw(self) -> None:
        # pg.draw.line(
        #    self.game.screen,
        #    'yellow',
        #    (self.x * 100, self.y * 100),
        #    (
        #        self.x * 100 + const.WIDTH * math.cos(self.angle),
        #        self.y * 100 + const.WIDTH * math.sin(self.angle)
        #    ),
        #    2,
        # )
        # draw field of view
        # for i in range(1, const.RAYS_NUM // 2 + 1):
        #    pg.draw.line(
        #        self.game.screen,
        #        'darkgray',
        #        (self.x * 100, self.y * 100),
        #        (
        #            self.x * 100 + const.WIDTH *
        #            math.cos(self.angle + const.DELTA_ANGLE * i),
        #            self.y * 100 + const.WIDTH *
        #            math.sin(self.angle + const.DELTA_ANGLE * i)
        #        ),
        #        2,
        #    )
        #    pg.draw.line(
        #        self.game.screen,
        #        'darkgray',
        #        (self.x * 100, self.y * 100),
        #        (
        #            self.x * 100 + const.WIDTH *
        #            math.cos(self.angle - const.DELTA_ANGLE * i),
        #            self.y * 100 + const.WIDTH *
        #            math.sin(self.angle - const.DELTA_ANGLE * i)
        #        ),
        #        2,
        #    )
        pg.draw.circle(
            self.game.screen,
            'green',
            (self.x * 100, self.y * 100),
            15,
        )

    def update(self) -> None:
        self.movement()

    # @property
    def pos(self) -> tuple[float, float]:
        return (self.x, self.y)

    # @property
    def map_pos(self) -> tuple[int, int]:
        return (int(self.x), int(self.y))
