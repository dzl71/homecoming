from player import Player
# import constants as const
from raycasting import RayCasting

p = Player()
r = RayCasting(p)

print(f"{r.vert_wall_distance(0) = }")
print()
print(f"{r.hor_wall_distance(0) = }")
