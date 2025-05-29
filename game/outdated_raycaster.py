import math
import numpy as np
import numpy.typing as npt
from .maze import WALL
from line_profiler import profile


# thanks to javidx9 video
class Raycaster:
    def __init__(self, cell_width: int, rays_amount: int, fov: int):
        self.cell_width = cell_width
        self.rays_amount = rays_amount
        self.fov = fov
        self.angle_step = self.fov / max(
            (self.rays_amount - 1), 1
        )  # min 1, prevent division by 0
        # no angle offset when only one ray, starts directly at player angle
        self.ray_angle_substraction = 0.0
        if self.rays_amount > 1:
            self.ray_angle_substraction = self.fov / 2

    def reset(self, maze_structure: npt.NDArray):
        self.maze_structure = np.array(maze_structure)

    # @profile
    def cast_multiple_rays(self, player_pos: tuple[float, float], player_angle: float):
        rays_length = []
        ray_angle = player_angle - self.ray_angle_substraction
        player_pos_normalised = np.array(player_pos) / 40
        player_maze_pos = np.array(
            [int(player_pos_normalised[0]), int(player_pos_normalised[1])]
        )
        for _ in range(self.rays_amount):
            ray = self.cast_single_ray(
                np.array(player_pos),
                player_pos_normalised,
                player_maze_pos,
                player_angle,
                ray_angle,
            )
            rays_length.append(ray)
            ray_angle += self.angle_step
        return rays_length

    # @profile
    def cast_single_ray(
        self,
        player_pos: npt.NDArray,
        player_pos_normalised: npt.NDArray,
        player_maze_pos: npt.NDArray,
        player_angle: float,
        ray_angle: float,
    ):
        if ray_angle == 0:
            ray_angle = 0.000001

        ray_maze_pos = player_maze_pos.copy()

        ray_dir_x = math.cos(ray_angle)
        ray_dir_y = math.sin(ray_angle)
        ray_length_step_x = math.sqrt(1 + math.pow((ray_dir_y / ray_dir_x), 2))
        ray_length_step_y = math.sqrt(1 + math.pow((ray_dir_x / ray_dir_y), 2))

        # looking left
        if ray_dir_x < 0:
            ray_step_x = -1
            ray_length_x = (
                player_pos_normalised[0] - ray_maze_pos[0]
            ) * ray_length_step_x
        # looking right
        else:
            ray_step_x = 1
            ray_length_x = (
                ray_maze_pos[0] + 1 - player_pos_normalised[0]
            ) * ray_length_step_x
        # looking up
        if ray_dir_y < 0:
            ray_step_y = -1
            ray_length_y = (
                player_pos_normalised[1] - ray_maze_pos[1]
            ) * ray_length_step_y
        # looking down
        else:
            ray_step_y = 1
            ray_length_y = (
                ray_maze_pos[1] + 1 - player_pos_normalised[1]
            ) * ray_length_step_y
        collision = False
        ray_length = 0.0
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
        ray_length *= self.cell_width
        no_fish_angle = player_angle - ray_angle
        no_fish_length = math.cos(no_fish_angle) * ray_length
        return no_fish_length
