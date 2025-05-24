import numpy.typing as npt
import pygame

WALL = 0
PATH = 1
GOAL = 2


class MazeRenderer:
    CELL_WIDTH = 40

    def __init__(self):
        self.path = pygame.Surface((self.CELL_WIDTH, self.CELL_WIDTH))
        self.path.fill("White")
        self.wall = self.path.copy()
        self.wall.fill("Black")
        self.goal = self.path.copy()
        self.goal.fill("Blue")
        self.current_rect = self.path.get_rect()

    def reset(self, maze_structure: npt.NDArray):
        image_width = self.CELL_WIDTH * len(maze_structure)
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
                self.current_rect.x += self.CELL_WIDTH
            self.current_rect.y += self.CELL_WIDTH

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image)
