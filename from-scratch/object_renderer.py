import pygame as pg
import constants as const


class ObjectRenderer:
    def __init__(self, screen) -> None:
        self.screen = screen
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
            # depth: float,
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
