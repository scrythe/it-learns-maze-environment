import pygame
from .maze import generate_maze_structure
from .maze import MazeRenderer
from .player import Player
from .actions import ActionEnum


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

    def draw(self, screen: pygame.Surface):
        # screen.fill("Black")
        self.maze_renderer.draw(screen)
        self.player.draw(screen)
        pygame.display.update()
