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
        self.map = game.map
        self.player = game.player
        self.screen = game.screen
        self.path_extention = ""
        self.set_textures()

    def set_textures(self):
        self.floor_ceil_pixel_grid = split_pixel_grid(
            Image.open(f"{const.TEXTURES_PATH}/{self.path_extention}1.png")
        )
        self.marked_floor_ceil_pixel_grid = split_pixel_grid(
            Image.open(
                f"{const.TEXTURES_PATH}/{self.path_extention}marked_texture.png")
        )
        self.default_texture: int = 1
        self.textures: dict[int, pg.Surface] = {
            1: self.get_texture(
                f"{const.TEXTURES_PATH}/{self.path_extention}1.png",
                (const.TEXTURE_SIZE, const.TEXTURE_SIZE),
            ),
            2: self.get_texture(
                f"{const.TEXTURES_PATH}/{self.path_extention}right_wall.png",
                (const.TEXTURE_SIZE, const.TEXTURE_SIZE),
            ),
            3: self.get_texture(
                f"{const.TEXTURES_PATH}/{self.path_extention}left_wall.png",
                (const.TEXTURE_SIZE, const.TEXTURE_SIZE),
            ),
            4: self.get_texture(
                f"{const.TEXTURES_PATH}/{self.path_extention}133.png",
                (const.TEXTURE_SIZE, const.TEXTURE_SIZE),
            ),
            5: self.get_texture(
                f"{const.TEXTURES_PATH}/{self.path_extention}bringthemhomenow.png",
                (const.TEXTURE_SIZE, const.TEXTURE_SIZE),
            ),
            6: self.get_texture(
                f"{const.TEXTURES_PATH}/{self.path_extention}3.png",
                (const.TEXTURE_SIZE, const.TEXTURE_SIZE),
            ),
            7: self.get_texture(
                f"{const.TEXTURES_PATH}/{self.path_extention}deadend.png",
                (const.TEXTURE_SIZE, const.TEXTURE_SIZE),
            ),
            8: self.get_texture(
                f"{const.TEXTURES_PATH}/{self.path_extention}emptiness.png",
                (const.TEXTURE_SIZE, const.TEXTURE_SIZE),
            ),
            9: self.get_texture(
                f"{const.TEXTURES_PATH}/{self.path_extention}bibas.png",
                (const.TEXTURE_SIZE, const.TEXTURE_SIZE),
            ),
            10: self.get_texture(
                f"{const.TEXTURES_PATH}/{self.path_extention}amit.png",
                (const.TEXTURE_SIZE, const.TEXTURE_SIZE),
            ),
            11: self.get_texture(
                f"{const.TEXTURES_PATH}/{self.path_extention}noa.png",
                (const.TEXTURE_SIZE, const.TEXTURE_SIZE),
            ),
            12: self.get_texture(
                f"{const.TEXTURES_PATH}/{self.path_extention}avinatan.png",
                (const.TEXTURE_SIZE, const.TEXTURE_SIZE),
            ),
            13: self.get_texture(
                f"{const.TEXTURES_PATH}/{self.path_extention}eden.png",
                (const.TEXTURE_SIZE, const.TEXTURE_SIZE),
            ),
            14: self.get_texture(
                f"{const.TEXTURES_PATH}/{self.path_extention}danzig.png",
                (const.TEXTURE_SIZE, const.TEXTURE_SIZE),
            ),
            -1: self.get_texture(
                f"{const.SPRITES_PATH}/{self.path_extention}prisoner.png",
                (const.TEXTURE_SIZE, const.TEXTURE_SIZE)
            ),
        }

    @staticmethod
    def get_texture(path: str, dimentions) -> pg.Surface:
        return pg.transform.scale(
            pg.image.load(path).convert_alpha(),
            dimentions
        )

    def render_texture_column(
            self,
            texture: int,
            offset: float,
            proj_height: float,
            ray: int,
            dimentions: tuple[int, int]
    ) -> None:
        if proj_height < const.HEIGHT:
            wall_column = self.textures[texture].subsurface(
                offset * (dimentions[0] - const.SCALE),
                0,
                const.SCALE,
                dimentions[1]
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
            texture_height: float = dimentions[1] * const.HEIGHT / proj_height
            wall_column = self.textures[texture].subsurface(
                offset * (dimentions[0] - const.SCALE),
                dimentions[1] // 2 - texture_height // 2,
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
            ray,
            max_pixel_position,
            ray_angle
    ) -> None:
        pixel_position = const.HEIGHT
        pixel_position_diff = 2  # the higher the number, the lower the quality
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
                pixel_position += pixel_position_diff
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

            # fill ceil pixel
            self.screen.fill(
                color,
                (
                    ray * const.SCALE,
                    const.HEIGHT - pixel_position,
                    const.SCALE,
                    pixel_position_diff
                )
            )

            if (int(floor_intersection_x), int(floor_intersection_y)) in self.map.marked:
                color = self.marked_floor_ceil_pixel_grid[texture_x][texture_y]

            # fill floor pixel
            self.screen.fill(
                color,
                (
                    ray * const.SCALE,
                    pixel_position,
                    const.SCALE,
                    pixel_position_diff
                )
            )

            # decrement to calculate next pixel
            pixel_position -= pixel_position_diff

# commit
