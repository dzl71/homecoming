import math
import pygame as pg
from PIL import Image
import constants as const


def calculate_color_intensity(distance):
    # Calculate intensity relative to distance
    return (1 - (distance / const.LONGEST_DISTANCE))**2


def split_pixel_grid(image: Image.Image):
    # Load pixel data from texture
    texture_data = image.load()

    # Iterate through each column and row and add pixel to list
    return [
        [
            texture_data[column, row] for row in range(image.height)
        ] for column in range(image.width)
    ]


class ObjectRenderer:
    def __init__(self, game) -> None:
        self.player = game.player
        self.screen = game.screen
        self.floor_ceil_pixel_grid = split_pixel_grid(
            Image.open("resources/textures/1.png")
        )
        self.wall_textures: dict[int, pg.Surface] = {
            1: self.get_texture("resources/textures/1.png")
        }

    @staticmethod
    def get_texture(path: str) -> pg.Surface:
        return pg.transform.scale(
            pg.image.load(path).convert_alpha(),
            (const.TEXTURE_SIZE, const.TEXTURE_SIZE)
        )

    def render_wall_column(
            self,
            texture: int,
            offset: float,
            proj_height: float,
            ray: int
    ) -> None:
        if proj_height < const.HEIGHT:
            wall_column = self.wall_textures[texture].subsurface(
                offset * (const.TEXTURE_SIZE - const.SCALE),
                0,
                const.SCALE,
                const.TEXTURE_SIZE
            )
            wall_column = pg.transform.scale(
                wall_column,
                (const.SCALE, proj_height)
            )
            wall_pos = (
                ray * const.SCALE,
                const.HALF_HEIGHT - proj_height // 2
            )
        else:
            texture_height: float = const.TEXTURE_SIZE * const.HEIGHT / proj_height
            wall_column = self.wall_textures[texture].subsurface(
                offset * (const.TEXTURE_SIZE - const.SCALE),
                const.HALF_TEXTURE_SIZE - texture_height // 2,
                const.SCALE,
                texture_height
            )
            wall_column = pg.transform.scale(
                wall_column,
                (const.SCALE, const.HEIGHT)
            )
            wall_pos = (ray * const.SCALE, 0)
        self.screen.blit(
            wall_column,
            wall_pos
        )

    def render_floor_ceil_column(
            self,
            screen,
            ray,
            max_pixel_position,
            ray_angle
    ) -> None:
        pixel_position = const.HEIGHT
        delta_pixel_position = 3
        cos_a: float = math.cos(ray_angle)
        sin_a: float = math.sin(ray_angle)
        # Continue to calculate pixels while on screen
        while pixel_position >= max_pixel_position:
            # Use pixel and camera position to find the straight distance from camera to floor intersection
            straight_distance: float = const.SCREEN_DISTANCE * \
                const.WALL_HEIGHT / 2 / (pixel_position - const.HALF_HEIGHT)

            # Calculate actual distance
            actual_distance = straight_distance / \
                math.cos(ray_angle - self.player.angle)

            if actual_distance > const.MAX_RAY_DEPTH:
                pixel_position += delta_pixel_position
                break

            # Calculate floor intersection
            floor_intersection_x = self.player.x + \
                (cos_a * actual_distance)
            floor_intersection_y = self.player.y + \
                (sin_a * actual_distance)

            # Find the correct texture index
            texture_x = math.floor(
                (floor_intersection_x % 1) * len(self.floor_ceil_pixel_grid)
            )
            texture_y = math.floor(
                (floor_intersection_y % 1) * len(self.floor_ceil_pixel_grid)
            )

            # Find corresponding color
            color = self.floor_ceil_pixel_grid[texture_x][texture_y]

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

            # decrement to calculate next pixel
            pixel_position -= delta_pixel_position
