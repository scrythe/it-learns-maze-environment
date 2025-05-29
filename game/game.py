import pygame

# from .maze.old_maze_structure import generate_maze_structure
from .maze import MazeRenderer
from .player import Player
from .maze import WALL
import math
from line_profiler import profile

from maze_env_rust import Raycaster, generate_maze_structure
import numpy as np

# from .outdated_raycaster import Raycaster


class Game:
    cell_width = 40
    player_radius = 10
    player_rotation_speed = 0.05
    player_movement_speed = 2
    rays_amount = 6
    fov = 1 / 2 * math.pi  # 90 degrees

    def __init__(self):
        self.maze_renderer = MazeRenderer(self.cell_width)
        self.player = Player(
            self.player_radius, self.player_rotation_speed, self.player_movement_speed
        )
        # self.raycaster = Raycaster(self.cell_width, self.rays_amount, self.fov)
        self.raycaster = Raycaster(self.cell_width, self.rays_amount, self.fov)
        self.rect = pygame.Rect()

    def draw_3d(self, screen: pygame.Surface):
        x = self.rect.width / 2 + self.ray_width_step / 2
        for ray in self.rays:
            object_length = min(self.object_height_factor / ray, self.rect.height)
            y = self.rect.height / 2 - object_length / 2
            pygame.draw.line(
                screen,
                "Green",
                (x, y),
                (x, y + object_length),
                math.ceil(self.ray_width_step),
            )
            x += self.ray_width_step

    # @profile
    def reset(self, size: int, seed: int):
        self.maze_structure = generate_maze_structure(size, seed)
        self.raycaster.reset(self.maze_structure)
        maze_width = self.cell_width * len(self.maze_structure)
        self.ray_width_step = (maze_width) / self.rays_amount
        self.object_height_factor = maze_width * self.player_radius
        self.player.reset()

    def _get_obs(self):
        self.rays = self.raycaster.cast_multiple_rays(
            self.player.rect.center, self.player.angle
        )
        return np.array(self.rays, dtype=np.float32)

    # @profile
    def step(self, action: int):
        self.player.step(action)
        collision = self.collision_detection()
        obs = self._get_obs()
        terminated = collision
        return obs, terminated

    def collision_detection(self):
        x_pos = int(self.player.rect.centerx / self.cell_width)
        y_pos = int(self.player.rect.centery / self.cell_width)

        # Check colliding with right cell
        # Should maybe check if index out of range, but unlikely to happen
        # because of borders
        if self.maze_structure[y_pos][x_pos + 1] == WALL:
            if int(self.player.rect.right / self.cell_width) == x_pos + 1:
                return True
                # self.player.rect.right = (x_pos + 1) * self.cell_width
        # Check colliding with left cell
        if self.maze_structure[y_pos][x_pos - 1] == WALL:
            if int(self.player.rect.left / self.cell_width) == x_pos - 1:
                return True
                # self.player.rect.left = x_pos * self.cell_width
        # Check colliding with above cell
        if self.maze_structure[y_pos - 1][x_pos] == WALL:
            if int(self.player.rect.top / self.cell_width) == y_pos - 1:
                return True
                # self.player.rect.top = y_pos * self.cell_width
        # Check colliding with below cell
        if self.maze_structure[y_pos + 1][x_pos] == WALL:
            if int(self.player.rect.bottom / self.cell_width) == y_pos + 1:
                return True
                # self.player.rect.bottom = (y_pos + 1) * self.cell_width
        return False

    def draw(self, screen: pygame.Surface):
        screen.fill("Black")
        self.maze_renderer.draw(screen)
        self.player.draw(screen)
        self.draw_3d(screen)
        pygame.display.update()
