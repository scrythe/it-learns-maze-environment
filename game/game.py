import pygame
from .maze import generate_maze_structure
from .maze import MazeRenderer
from .player import Player
from .actions import ActionEnum
from .maze import WALL


class Game:
    cell_width = 40
    player_radius = 10
    player_rotation_speed = 0.05
    player_movement_speed = 2

    def __init__(self):
        self.maze_renderer = MazeRenderer(self.cell_width)
        self.player = Player(
            self.player_radius, self.player_rotation_speed, self.player_movement_speed
        )

    def reset(self, size):
        self.maze_structure = generate_maze_structure(size)
        self.maze_renderer.reset(self.maze_structure)
        self.rect = self.maze_renderer.image.get_rect()
        self.player.reset()

    def step(self, action: int):
        action_enum = ActionEnum(action)
        self.player.step(action_enum)
        collision = self.collision_detection()
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
        # screen.fill("Black")
        self.maze_renderer.draw(screen)
        self.player.draw(screen)
        pygame.display.update()
