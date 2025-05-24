import pygame
from .maze import generate_maze_structure
from .maze import MazeRenderer
from .player import Player
from .actions import ActionEnum

WALL = 0


class Game:
    def __init__(self):
        self.maze_renderer = MazeRenderer()
        self.player = Player()

    def reset(self, size):
        self.maze_structure = generate_maze_structure(size)
        self.maze_renderer.reset(self.maze_structure)
        self.rect = self.maze_renderer.image.get_rect()
        self.player.reset()

    def step(self, action: ActionEnum):
        self.player.step(action)
        self.collision()

    def collision(self):
        x_pos = int(self.player.rect.centerx / 40)
        y_pos = int(self.player.rect.centery / 40)
        # Check colliding with right cell
        if self.maze_structure[y_pos, x_pos + 1] == WALL:
            if int(self.player.rect.right / 40) == x_pos + 1:
                self.player.rect.right = (x_pos + 1) * 40
        # Check colliding with left cell
        if self.maze_structure[y_pos, x_pos - 1] == WALL:
            if int(self.player.rect.left / 40) == x_pos - 1:
                self.player.rect.left = x_pos * 40
        # Check colliding with above cell
        if self.maze_structure[y_pos - 1, x_pos] == WALL:
            if int(self.player.rect.top / 40) == y_pos - 1:
                self.player.rect.top = y_pos * 40
        # Check colliding with below cell
        if self.maze_structure[y_pos + 1, x_pos] == WALL:
            if int(self.player.rect.bottom / 40) == y_pos + 1:
                self.player.rect.bottom = (y_pos + 1) * 40

    def draw(self, screen: pygame.Surface):
        # screen.fill("Black")
        self.maze_renderer.draw(screen)
        self.player.draw(screen)
        pygame.display.update()
