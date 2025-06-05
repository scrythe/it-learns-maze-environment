import pygame

from .maze import MazeRenderer
from .player import Player
from .maze import WALL, PATH
import math

from maze_env_rust import Raycaster, generate_maze_structure
import numpy as np


class Game:
    cell_width = 40
    player_radius = 10
    player_rotation_speed = 0.05
    player_movement_speed = 2
    rays_amount = 6
    fov = 1 / 2 * math.pi  # 90 degrees
    total_life_time = 50

    def __init__(self):
        self.maze_renderer = MazeRenderer(self.cell_width)
        self.player = Player(
            self.player_radius, self.player_rotation_speed, self.player_movement_speed
        )
        # self.raycaster = Raycaster(self.cell_width, self.rays_amount, self.fov)
        self.raycaster = Raycaster(self.cell_width, self.rays_amount, self.fov)
        self.rect = pygame.Rect()
        # self.life_time = total_life_time

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
        self.maze_structure, maze_start = generate_maze_structure(size, seed)
        if pygame.display.get_init():
            self.maze_renderer.reset(self.maze_structure)
            self.rect = self.maze_renderer.image.get_rect()
            self.rect.width *= 2
        self.raycaster.reset(self.maze_structure)
        maze_width = self.cell_width * len(self.maze_structure)
        self.ray_width_step = (maze_width) / self.rays_amount
        self.object_height_factor = maze_width * self.player_radius
        start = [maze_start[0] * self.cell_width, maze_start[1] * self.cell_width]
        self.player.reset(start)
        self.life_time = self.total_life_time
        self.rays = self.raycaster.cast_multiple_rays(
            self.player.rect.center, self.player.angle
        )
        maze_structure_size = len(self.maze_structure)
        self.visited_cells = np.zeros(
            (maze_structure_size, maze_structure_size), dtype=np.bool
        )
        self.collision = False

    # @profile
    def step(self, action: int):
        self.player.step(action)
        self.collision = self.collision_detection()
        new_path = self.check_new_path()
        if new_path:
            self.life_time += 35
        self.rays = self.raycaster.cast_multiple_rays(
            self.player.rect.center, self.player.angle
        )
        self.life_time -= 1
        return new_path

    def check_new_path(self):
        x_pos = int(self.player.rect.centerx / self.cell_width)
        y_pos = int(self.player.rect.centery / self.cell_width)
        if self.maze_structure[y_pos][x_pos] == PATH:
            if not self.visited_cells[y_pos][x_pos]:
                self.visited_cells[y_pos][x_pos] = True
                return True

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
