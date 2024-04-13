import math
import pygame as pg
import constants as const
from map import Map
from player import Player
from PIL import Image


longest_distance = math.sqrt(
    len(const.MAP)**2 + len(const.MAP[0])**2)


def calculate_color_intensity(distance):
    # Calculate intensity relative to distance
    return (1 - (distance / longest_distance))**2


def split_pixel_grid(image: Image.Image):
    # Load pixel data from texture
    texture_data = image.load()

    # Iterate through each column and row and add pixel to list
    return [
        [
            texture_data[column, row] for row in range(image.height)
        ] for column in range(image.width)
    ]


floor_pixel_grid = split_pixel_grid(Image.open("resources/textures/1.png"))


def pos_cos(angle: float) -> bool:
    return (
        0 <= angle % math.tau < math.pi / 2 or math.pi * 1.5 < angle % math.tau
    )


def pos_sin(angle: float) -> bool:
    return 0 < angle % math.tau < math.pi


class RayCasting:
    def __init__(self, game) -> None:
        # self.game = game
        self.map: Map = game.map  # placeholder value
        self.player: Player = game.player
        self.object_renderer = game.object_renderer

    def vert_wall_distance(self, ray_angle: float) -> tuple[float, int, float]:
        '''
        @ray_angle
            the angle of the sended ray (in radians)

        @return
             tuple(
                 the distance to the vertical intersection with a wall,
                 the enumeration of the wall texture,
                 y value of the intersection
             )

        '''
        # caching repeated calculations to decrese calculation amount
        # adding a small value to the angle to avoid division by zero
        ray_angle += 1e-6
        cos_a: float = math.cos(ray_angle)
        sin_a: float = math.sin(ray_angle)

        # calculating the x of first intersection and the delta_x of the following intersections
        intersect_x: int
        delta_x: float
        if pos_cos(ray_angle):
            delta_x = 1
            intersect_x = math.ceil(self.player.x)
        else:
            delta_x = -1
            intersect_x = math.floor(self.player.x) - 1e-6

        # calculating the depth of first intersection and the delta_depth of the following intersections
        depth: float = (intersect_x - self.player.x) / cos_a
        delta_depth: float = delta_x / cos_a

        # calculating the y of first intersection and the delta_y of the following intersections
        delta_y: float = delta_depth * sin_a
        intersect_y: float = self.player.y + depth * sin_a

        # if ray_angle == self.player.angle - const.HALF_FOV + 1e-6:
        # print(
        #     f"initial_vert_{intersect_x = }, initial_vert_{intersect_y = }"
        # )

        # sending the ray deeper until collision accures, or exiting the bounds
        texture: int = 1  # default texture
        for _ in range(const.MAX_RAY_DEPTH):
            tile: tuple[int, int] = (int(intersect_y), int(intersect_x))
            if tile in self.map.wall_positions:
                texture = self.map.wall_positions[tile]
                break
            intersect_x += delta_x
            intersect_y += delta_y
            depth += delta_depth

        # if ray_angle == self.player.angle - const.HALF_FOV + 1e-6:
        #     print(f"vert_{intersect_x = }, vert_{intersect_y = }\n")

        return (depth, texture, intersect_y)

    def hor_wall_distance(self, ray_angle: float) -> tuple[float, int, float]:
        '''
        @ray_angle
            the angle of the sended ray (in radians)

        @return
             tuple(
                the distance to the horizontal intersection with a wall,
                the enumeration of the wall texture,
                x value of the intersection
             )

        '''
        # caching repeated calculations to decrese calculation amount
        # adding a small value to the angle to avoid division by zero
        ray_angle += 1e-6
        sin_a: float = math.sin(ray_angle)
        cos_a: float = math.cos(ray_angle)

        # calculating the y of first intersection and the delta_y of the following intersections
        delta_y: float
        intersect_y: int
        if pos_sin(ray_angle):
            delta_y = 1
            intersect_y = math.ceil(self.player.y)
        else:
            delta_y = -1
            intersect_y = math.floor(self.player.y) - 1e-6

        # calculating the depth of first intersection and the delta_depth of the following intersections
        depth: float = (intersect_y - self.player.y) / sin_a
        delta_depth: float = delta_y / sin_a

        # calculating the x of first intersection and the delta_x of the following intersections
        delta_x: float = delta_depth * cos_a
        intersect_x: float = self.player.x + depth * cos_a

        # if ray_angle == self.player.angle - const.HALF_FOV + 1e-6:
        #     print(
        #         f"initial_hor_{intersect_x = }, initial_hor_{intersect_y = }"
        #     )

        # sending the ray deeper until collision accures, or exiting the bounds
        texture: int = 1  # default texture
        for _ in range(const.MAX_RAY_DEPTH):
            tile: tuple[int, int] = (int(intersect_y), int(intersect_x))
            if tile in self.map.wall_positions:
                texture = self.map.wall_positions[tile]
                break
            intersect_x += delta_x
            intersect_y += delta_y
            depth += delta_depth

        # if ray_angle == self.player.angle - const.HALF_FOV + 1e-6:
        #     print(f"hor_{intersect_x = }, hor_{intersect_y = }\n")

        return (depth, texture, intersect_x)

    def draw_floor_ceiling(self, screen, ray, pixel_position, ray_angle):
        delta_pixel_position = 3
        cos_a: float = math.cos(ray_angle)
        sin_a: float = math.sin(ray_angle)
        # Continue to calculate pixels while on screen
        while pixel_position < const.HEIGHT:
            # Use pixel and camera position to find the straight distance from camera to floor intersection
            pixel_distance_to_center = pixel_position - const.HALF_HEIGHT
            straight_distance = const.SCREEN_DISTANCE * \
                const.WALL_HEIGHT / 2 / pixel_distance_to_center
            # Calculate actual distance
            actual_distance = straight_distance / \
                math.cos(ray_angle - self.player.angle)

            if actual_distance > const.MAX_RAY_DEPTH:
                pixel_position += delta_pixel_position
                continue

            # Calculate floor intersection
            floor_intersection_x = self.player.x + \
                (cos_a * actual_distance)
            floor_intersection_y = self.player.y + \
                (sin_a * actual_distance)

            # Find the correct texture index
            texture_x = math.floor(
                (floor_intersection_x % 1) * len(floor_pixel_grid)
            )
            texture_y = math.floor(
                (floor_intersection_y % 1) * len(floor_pixel_grid)
            )

            # Find corresponding color
            color = floor_pixel_grid[texture_x][texture_y]

            # Adjust color according to distance
            intensity = calculate_color_intensity(actual_distance)
            adjusted_color = tuple(
                color_value * intensity for color_value in color
            )

            # Fill in the pixel
            screen.fill(
                adjusted_color,
                (
                    ray * const.SCALE,
                    const.HEIGHT - pixel_position,
                    const.SCALE,
                    delta_pixel_position
                )
            )
            screen.fill(
                adjusted_color,
                (
                    ray * const.SCALE,
                    pixel_position,
                    const.SCALE,
                    delta_pixel_position
                )
            )

            # Increment to calculate next pixel underneath
            pixel_position += delta_pixel_position

    def ray_cast(self, screen) -> None:
        ray_angle: float = self.player.angle - const.HALF_FOV + 1e-6
        for ray in range(const.RAY_NUM):

            vert_depth: float
            vert_texture: int
            vert_y: float
            (vert_depth, vert_texture, vert_y) = self.vert_wall_distance(ray_angle)
            hor_depth: float
            hor_texture: int
            hor_x: float
            (hor_depth, hor_texture, hor_x) = self.hor_wall_distance(ray_angle)

            ray_depth: float
            offset: float
            texture: int
            if vert_depth < hor_depth:
                texture = vert_texture
                ray_depth = vert_depth
                vert_y %= 1
                offset = vert_y if pos_cos(ray_angle) else 1 - vert_y
            else:
                texture = hor_texture
                ray_depth = hor_depth
                hor_x %= 1
                offset = hor_x if not pos_sin(ray_angle) else 1 - hor_x

            # if ray_angle == self.player.angle - const.HALF_FOV + 1e-6:
            #     print(f"{ray_angle = }")
            #     print(f"{self.vert_wall_distance(ray_angle) = }")
            #     print(f"{self.hor_wall_distance(ray_angle) = }")
            #     print(f"{ray_depth = }")
            #     print("\n====================================================\n")

            # remove the fishblow effect
            ray_depth *= math.cos(self.player.angle - ray_angle)

            # projection height
            proj_height = const.SCREEN_DISTANCE / (ray_depth + 1e-6)

            self.draw_floor_ceiling(
                screen,
                ray,
                const.HALF_HEIGHT + proj_height // 2 - 1,
                ray_angle
            )

            if ray_depth >= const.MAX_RAY_DEPTH:
                ray_angle += const.DELTA_ANGLE
                continue

            self.object_renderer.render_wall_column(
                texture,
                offset,
                proj_height,
                ray
            )

            # pg.draw.line(
            #     screen,
            #     'darkgray',
            #     (self.player.x * 100, self.player.y * 100),
            #     (self.player.x * 100 + ray_depth * 100 * math.cos(ray_angle),
            #         self.player.y * 100 + ray_depth * 100 * math.sin(ray_angle)),
            #     2,
            # )

            ray_angle += const.DELTA_ANGLE
