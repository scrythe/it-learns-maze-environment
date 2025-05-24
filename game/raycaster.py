import math
import numpy as np
import numpy.typing as npt
from .maze import WALL


# thanks to javidx9 video
class Raycaster:
    def __init__(self):
        pass

    def cast_multiple_rays(self):
        pass

    def cast_single_ray(
        self, maze_structure: npt.NDArray, player_pos: tuple[float, float], angle: float
    ):
        player_pos_normal = np.array(player_pos) / 40
        ray_pos = player_pos_normal.copy()
        ray_dir_x = math.cos(angle)
        ray_dir_y = math.sin(angle)
        if ray_dir_x == 0:
            ray_length_step_x = 1.0
        else:
            ray_length_step_x = math.sqrt(1 + math.pow((ray_dir_y / ray_dir_x), 2))
        if ray_dir_y == 0:
            ray_length_step_y = 1.0
        else:
            ray_length_step_y = math.sqrt(1 + math.pow((ray_dir_x / ray_dir_y), 2))
        # looking left
        if math.pi / 2 < angle < 3 * math.pi / 2:
            ray_step_x = -1
            ray_length_x = (
                player_pos_normal[0] - int(player_pos_normal[0])
            ) * ray_length_step_x
        # looking right
        else:
            ray_step_x = 1
            ray_length_x = (
                int(player_pos_normal[0]) + 1 - player_pos_normal[0]
            ) * ray_length_step_x
        # looking down
        if 0 < angle < math.pi:
            ray_step_y = 1
            ray_length_y = (
                int(player_pos_normal[1] + 1) - player_pos_normal[1]
            ) * ray_length_step_y
        # looking up
        else:
            ray_step_y = -1
            ray_length_y = (
                player_pos_normal[1] - int(player_pos_normal[1])
            ) * ray_length_step_y
        collision = False
        ray_length = 0
        # ray_pos -= 1
        while not collision:
            if ray_length_x > ray_length_y:
                ray_pos[1] += ray_step_y
                ray_length = ray_length_y
                ray_length_y += ray_length_step_y
            else:
                ray_pos[0] += ray_step_x
                ray_length = ray_length_x
                ray_length_x += ray_length_step_x
            ray_maze_pos = int(ray_pos[0]), int(ray_pos[1])
            if maze_structure[ray_maze_pos[1], ray_maze_pos[0]] == WALL:
                print(ray_maze_pos)
                collision = True
        return ray_pos * 40
        # print(ray_length)
