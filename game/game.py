import pygame
from .maze import generate_maze_structure
from .maze import MazeRenderer


class Game:
    def __init__(self):
        self.maze = MazeRenderer()

    def reset(self, size):
        self.maze_structure = generate_maze_structure(size)
        self.maze.reset(self.maze_structure)

    def perform_action(self, action):
        pass

    def draw(self, screen: pygame.Surface):
        screen.fill("Black")
        pygame.display.update()
