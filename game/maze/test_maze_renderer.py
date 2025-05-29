from .maze_structure import generate_maze_structure
from .maze_renderer import MazeRenderer
import pygame
import pytest
import numpy as np


# @pytest.mark.skip(reason="don't want to test everytime")
def test_maze():
    size = 12
    maze_structure = generate_maze_structure(size, np.random.SeedSequence().entropy)
    maze_renderer = MazeRenderer(40)
    maze_renderer.reset(maze_structure)

    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode(
        (maze_renderer.image.width, maze_renderer.image.height)
    )
    maze_renderer.draw(screen)
    pygame.display.update()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
