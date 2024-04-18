import platform
import math

WIDTH: int = 1080
HEIGHT: int = 500
if platform.system() == "Linux":
    WIDTH = 1900
    HEIGHT = 1000
HALF_WIDTH: int = WIDTH // 2
HALF_HEIGHT: int = HEIGHT // 2
RESOLUTION: tuple[int, int] = (WIDTH, HEIGHT)

FPS: int = 60

MAP = [
    "##MM##################DD##########",
    "##            bb##    ##      DD",
    "##            tt##  LL##  LL####",  # (2,1)
    "##                            ##",
    "######################  RR  RR##",
    "###DD#########bb######  ##  ####",
    "##    ##        oo####  ##  ####",  # (7,8)
    "##    ##          ####  ##  ####",
    "##    ##          ####  ##  ####",
    "##    ##          ####  ##  ####",
    "RR  ##RR  ############  ##  ####",
    "##                          ####",
    "##LL  ##############  ttRR######",
    "####  ##EE        ##  ##      ##",
    "####  ####        ##  ##  ##  RR",
    "####  ######RR  LL##  ##  ##  ##",
    "##                    ##  ##  ##",
    "##########  ########  ##  ##  EE",
    "##DD##DD##            ##  ##  ##",
    "##  ##  ####RR######  ##  LL  ##",
    "##  ##    ##    DD##      ##  ##",  # (X,Y)
    "##  ##    ##  ######  LL####DD##",
    "##  ####  RR  ######  ##########",
    "RR                    ####tt####",
    "##    ##############  ##      ##",
    "##    ##oo        ##  ##      ##",
    "####  ##tt        ##  ##  oo  ##",  # (X,Y)
    "##      ##        ##  ##  ##  ##",
    "##      RR            ##  ##  ##",
    "##      ##########RR  ##  ##  ##",
    "##      ############  ##  ##  ##",
    "RR                    ##  ##  ##",
    "####################  ##  ##  ##",
    "####################  ##  ##  ##",
    "####################          LL",
    "####################  LL########",
    "####################  ####EE####",
    "##########bb          ##      ##",
    "############  ####RR  ##      ##",
    "##  oo##              ##      ##",
    "##    ##              ##      ##",  # (x,y)
    "##    ##    ######RR          LL",
    "RR        ##########LL        RR",
    "####tt######################  ##",
    "##oo    ##EE################  ##",
    "bb      ##          DD######  ##",
    "##      ##    ##############  ##",  # (x,y)  left
    "##      RR    ##############  ##",
    "RR                            ##",
    "##########################RR  ##",
    "tt                            ##",
    "bb                        ##RR##",
    "############EE########RR########",
]

MAP_WIDTH_MITIGATION: int = 2

MAP_SYMBOL_MEANING = {
    '#': 1,
    " ": 0,
    'R': 2,
    'L': 3,
    'o': -1,
    't': 4,
    'b': 5,
    'M': 6,
    'D': 7,
    'E': 8,
}

HOSTAGES_PLACED: int = 4

STARTING_ANGLE = 0
STARTING_X = 1.5
STARTING_Y = 2
PLAYER_SIZE_SCALE = 30

MAX_RAY_DEPTH = 16
FOV = math.pi / 3  # in radians
HALF_FOV = FOV / 2
RAY_NUM = WIDTH // 5
HALF_RAY_NUM = RAY_NUM // 2
DELTA_ANGLE = FOV / RAY_NUM

PLAYER_MOVEMENT_SPEED: float = 0.004
PLAYER_ROTATION_SPEED: float = 0.0025

SCREEN_DISTANCE: float = HALF_WIDTH / math.tan(HALF_FOV)
WALL_HEIGHT = 1
SCALE = WIDTH // RAY_NUM

TEXTURE_SIZE: int = 255
HALF_TEXTURE_SIZE: int = TEXTURE_SIZE // 2

LONGEST_DISTANCE: float = math.sqrt(
    len(MAP)**2 + (len(MAP[0]) / MAP_WIDTH_MITIGATION)**2
)

GAME_TIME: int = 150  # in seconds
FONT = 'JetBrains mono nerd'
FONT_SIZE = 40

MAP_SCALER: int = 100
MAP_HALF_WIDTH: int = math.ceil(HALF_WIDTH / MAP_SCALER)
MAP_HALF_HEIGHT: int = math.ceil(HALF_HEIGHT / MAP_SCALER)

MOUSE_SENSETIVITY: float = 1  # lower == faster

FAIL_MAIN_MESSAGE = "MISSION FAILED"
FAIL_SUB_MESSAGE = "Failed to rescue hostages on time"

SUCCESS_MAIN_MESSAGE = "MISSION SUCCESSFUL"
SUCCESS_SUB_MESSAGE = "All hostages rescued!"

CRIT_COLOR = (255, 0, 0)
REGULAR_COLOR = (255, 255, 255)


