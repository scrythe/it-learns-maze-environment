import pygame
from .maze import generate_maze_structure
from .maze import MazeRenderer
from .player import Player
from .actions import ActionEnum
from .maze import WALL
from .raycaster import Raycaster
import math


class Game:
    cell_width = 40
    player_radius = 10
    player_rotation_speed = 0.05
    player_movement_speed = 2
    rays_amount = 25
    fov = 1 / 2 * math.pi  # 90 degrees
    rect_height_factor = 20

    def __init__(self):
        self.maze_renderer = MazeRenderer(self.cell_width)
        self.player = Player(
            self.player_radius, self.player_rotation_speed, self.player_movement_speed
        )
        self.raycaster = Raycaster(self.cell_width, self.rays_amount, self.fov)

    def draw_ray(self, screen: pygame.Surface):
        if hasattr(self, "rays"):
            for ray in self.rays:
                pygame.draw.line(screen, "Red", self.player.rect.center, ray[0])

    def draw_3d(self, screen: pygame.Surface):
        if hasattr(self, "rays"):
            x = self.rect.width / 2 + self.ray_width_step / 2
            for ray in self.rays:
                ray_length = ray[1]
                object_length = min(
                    self.object_height_factor / ray_length, self.rect.height
                )
                y = self.rect.height / 2 - object_length / 2
                pygame.draw.line(
                    screen,
                    "Green",
                    (x, y),
                    (x, y + object_length),
                    math.ceil(self.ray_width_step),
                )
                x += self.ray_width_step

    def reset(self, size):
        self.maze_structure = generate_maze_structure(size)
        self.maze_renderer.reset(self.maze_structure)
        self.raycaster.reset(self.maze_structure)
        self.rect = self.maze_renderer.image.get_rect()
        self.rect.width *= 2
        self.ray_width_step = (self.rect.width / 2) / self.rays_amount
        self.object_height_factor = self.rect.height * self.rect_height_factor
        self.player.reset()

    def step(self, action: int):
        action_enum = ActionEnum(action)
        self.player.step(action_enum)
        collision = self.collision_detection()
        self.rays = self.raycaster.cast_multiple_rays(
            self.player.rect.center, self.player.angle
        )
        terminated = collision
        return terminated

    def collision_detection(self):
        x_pos = int(self.player.rect.centerx / self.cell_width)
        y_pos = int(self.player.rect.centery / self.cell_width)

        # Check colliding with right cell
        # Should maybe check if index out of range, but unlikely to happen
        # because of borders
        if self.maze_structure[y_pos, x_pos + 1] == WALL:
            if int(self.player.rect.right / self.cell_width) == x_pos + 1:
                return True
                # self.player.rect.right = (x_pos + 1) * self.cell_width
        # Check colliding with left cell
        if self.maze_structure[y_pos, x_pos - 1] == WALL:
            if int(self.player.rect.left / self.cell_width) == x_pos - 1:
                return True
                # self.player.rect.left = x_pos * self.cell_width
        # Check colliding with above cell
        if self.maze_structure[y_pos - 1, x_pos] == WALL:
            if int(self.player.rect.top / self.cell_width) == y_pos - 1:
                return True
                # self.player.rect.top = y_pos * self.cell_width
        # Check colliding with below cell
        if self.maze_structure[y_pos + 1, x_pos] == WALL:
            if int(self.player.rect.bottom / self.cell_width) == y_pos + 1:
                return True
                # self.player.rect.bottom = (y_pos + 1) * self.cell_width
        return False

    def draw(self, screen: pygame.Surface):
        screen.fill("Black")
        self.maze_renderer.draw(screen)
        self.player.draw(screen)
        self.draw_ray(screen)
        self.draw_3d(screen)
        pygame.display.update()
