import random
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
        if keys[pg.K_w] and not self.game.options.displaying_map:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s] and not self.game.options.displaying_map:
            dx -= speed_cos
            dy -= speed_sin
        if keys[pg.K_a] and not self.game.options.displaying_map:
            dx += speed_sin
            dy -= speed_cos
        if keys[pg.K_d] and not self.game.options.displaying_map:
            dx -= speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)

        x_movement, _ = pg.mouse.get_rel()
        if not self.game.options.displaying_map:
            self.angle += (
                const.PLAYER_ROTATION_SPEED
                # * self.game.delta_time
                * x_movement
                / const.MOUSE_SENSETIVITY
            )

        if keys[pg.K_LEFT] and not self.game.options.displaying_map:
            self.angle -= const.PLAYER_ROTATION_SPEED * self.game.delta_time

        if keys[pg.K_RIGHT] and not self.game.options.displaying_map:
            self.angle += const.PLAYER_ROTATION_SPEED * self.game.delta_time

        self.angle %= math.tau

        if keys[pg.K_v]:
            if not self.game.options.displaying_map and self.game.options.map_usages > 0:
                self.game.options.displaying_map = True
                self.game.options.map_usages -= 1
            else:
                self.game.options.displaying_map = False
            time.sleep(0.08)

        if keys[pg.K_f]:
            if self.game.options.pathfinding_usages > 0:
                self.find_path()

        self.remove_colided_sprites()

    def find_path(self) -> None:
        pos = (
            int(self.x),
            int(self.y),
        )
        movements = [
            (-1, 0),  # left
            (0, -1),  # up
            (0, 1),  # down
            (1, 0),  # right
        ]
        for movement in movements:
            if pos not in self.game.map.walls:
                break
            pos = (
                pos[0] + movement[0],
                pos[1] + movement[1],
            )
        self.game.pathfinding_tile = self.game.pathfinding.get_path(
            pos,
            self.game.searched_hostage
        )
        self.game.map.marked.add(self.game.pathfinding_tile)
        self.game.options.pathfinding_usages -= 1

    def check_wall(self, x: int, y: int) -> bool:
        return (x, y) not in self.game.map.walls

    def check_wall_collision(self, dx: float, dy: float) -> None:
        scale = const.PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def remove_colided_sprites(self) -> None:
        pos = (int(self.x), int(self.y))
        if pos in self.game.map.hostages:
            self.game.map.hostages.pop(pos)
            self.game.pathfinding.graph.clear()
            self.game.pathfinding.get_graph()
            self.game.map.marked.clear()
            self.game.searched_hostage = random.choice(
                list(self.game.map.hostages)
            )
            self.game.options.hostages_to_rescue -= 1

# comment to commit
