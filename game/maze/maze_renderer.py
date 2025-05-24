import numpy.typing as npt
import pygame
from .constants import PATH


class MazeRenderer:
    def __init__(self, cell_width):
        self.cell_width = cell_width
        self.path = pygame.Surface((self.cell_width, self.cell_width))
        self.path.fill("White")
        self.wall = self.path.copy()
        self.wall.fill("Black")
        self.goal = self.path.copy()
        self.goal.fill("Blue")
        self.current_rect = self.path.get_rect()

    def reset(self, maze_structure: npt.NDArray):
        image_width = self.cell_width * len(maze_structure)
        self.image = pygame.Surface((image_width, image_width))
        self.create_maze_image(maze_structure)

    def create_maze_image(self, maze_structure: npt.NDArray):
        self.current_rect.y = 0
        for row in maze_structure:
            self.current_rect.x = 0
            for cell in row:
                if cell == PATH:
                    self.image.blit(self.path, self.current_rect)
                else:
                    self.image.blit(self.wall, self.current_rect)
                self.current_rect.x += self.cell_width
            self.current_rect.y += self.cell_width

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image)
