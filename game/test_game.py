from .game import Game
import pygame
from .actions import ActionEnum
import numpy as np
import pytest


@pytest.mark.skip(reason="don't want to test everytime")
def test_game():
    game = Game()
    size = 10
    game.reset(size, np.random.default_rng())

    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode((game.rect.width, game.rect.height))
    running = True
    clock = pygame.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            game.step(0)
        elif keys[pygame.K_d]:
            game.step(1)
        elif keys[pygame.K_w]:
            game.step(2)

        game.draw(screen)
        pygame.display.update()
        clock.tick(60)
