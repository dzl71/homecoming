# the constants that will be used through out the project
import math

WIDTH: int = 1600
HEIGHT: int = 900
RESOLUTION: tuple[int, int] = (WIDTH, HEIGHT)
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
HALF_RESOLUTION = (HALF_WIDTH, HALF_HEIGHT)

FPS: int = 60

_ = False


# the map resolution should be WIDTH:HEIGHT
MAP: list[list[int]] = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, 1, 1, 1, 1, 1, 1, _, _, _, _, 1],
    [1, _, _, _, _, 1, _, _, _, _, 1, _, _, _, _, 1],
    [1, _, _, _, _, 1, _, _, _, _, 1, _, _, _, _, 1],
    [1, _, _, _, _, 1, 1, 1, 1, 1, 1, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

PLAYER_POS: tuple[float, float] = (1, 1)
PLAYER_ANGLE: float = 0
PLAYER_MOVEMENT_SPEED: float = 0.004
PLAYER_ROTATION_SPEED: float = 0.002

FIELD_OF_VIEW = math.pi / 3
HALF_FOV = FIELD_OF_VIEW / 2
RAYS_NUM = WIDTH // 2  # more rays == smoother walls
HALF_RAYS_NUM = RAYS_NUM // 2
DELTA_ANGLE = FIELD_OF_VIEW / RAYS_NUM
MAX_DEPTH = 30

SCREEN_DISTANCE = HALF_WIDTH / math.tan(HALF_FOV)
WALL_HEIGHT = 1
SCALE = WIDTH // RAYS_NUM
