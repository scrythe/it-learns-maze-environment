import pygame
from .maze import generate_maze_structure


class Game:
    def __init__(self):
        pass

    def reset(self, size):
        self.maze_structure = generate_maze_structure(size)

    def perform_action(self, action):
        pass

    def draw(self, screen: pygame.Surface):
        screen.fill("Black")
        pygame.display.update()
