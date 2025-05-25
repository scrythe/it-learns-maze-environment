import math
import numpy as np
import numpy.typing as npt
from .maze import WALL


# thanks to javidx9 video
class Raycaster:
    def __init__(self, cell_width: int):
        self.cell_width = cell_width

    def reset(self, maze_structure: npt.NDArray):
        self.maze_structure = maze_structure

    def cast_multiple_rays(self):
        pass

    def cast_single_ray(self, player_pos: tuple[float, float], angle: float):
        if angle == 0:
            angle = 0.000001
        player_pos_normalised = np.array(player_pos) / 40
        ray_start_pos = player_pos_normalised
        ray_maze_pos = np.array([int(ray_start_pos[0]), int(ray_start_pos[1])])
        ray_dir_x = math.cos(angle)
        ray_dir_y = math.sin(angle)
        ray_length_step_x = math.sqrt(1 + math.pow((ray_dir_y / ray_dir_x), 2))
        ray_length_step_y = math.sqrt(1 + math.pow((ray_dir_x / ray_dir_y), 2))
        # looking left
        if ray_dir_x < 0:
            ray_step_x = -1
            ray_length_x = (ray_start_pos[0] - ray_maze_pos[0]) * ray_length_step_x
        # looking right
        else:
            ray_step_x = 1
            ray_length_x = (ray_maze_pos[0] + 1 - ray_start_pos[0]) * ray_length_step_x
        # looking up
        if ray_dir_y < 0:
            ray_step_y = -1
            ray_length_y = (ray_start_pos[1] - ray_maze_pos[1]) * ray_length_step_y
        # looking down
        else:
            ray_step_y = 1
            ray_length_y = (ray_maze_pos[1] + 1 - ray_start_pos[1]) * ray_length_step_y
        collision = False
        ray_length = 0
        while not collision:
            if ray_length_x > ray_length_y:
                ray_maze_pos[1] += ray_step_y
                ray_length = ray_length_y
                ray_length_y += ray_length_step_y
            else:
                ray_maze_pos[0] += ray_step_x
                ray_length = ray_length_x
                ray_length_x += ray_length_step_x
            if self.maze_structure[ray_maze_pos[1], ray_maze_pos[0]] == WALL:
                collision = True
        ray_end = player_pos + ray_length * np.array([ray_dir_x, ray_dir_y]) * 40
        return ray_end

    # def cast_straight_ray(
    #     self,
    #     player_pos,
    #     ray_maze_pos,
    #     axis,
    #     ray_step_axis,
    #     ray_length_axis,
    # ):
    #     collision = False
    #     while not collision:
    #         ray_maze_pos[axis] += ray_step_axis
    #         ray_length = ray_length_axis.copy()
    #         ray_length_axis += 1
    #         if self.maze_structure[ray_maze_pos[1], ray_maze_pos[0]] == WALL:
    #             collision = True
    #     total_ray = [ray_length, ray_length]
    #     total_ray[1 - axis] = 0
    #     ray_end = player_pos + np.array(total_ray) * 40
    #     return ray_end
