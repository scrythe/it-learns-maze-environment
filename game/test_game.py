from .game import Game
import pygame
import pytest
from .actions import ActionEnum


@pytest.mark.skip(reason="don't want to test everytime")
def test_game():
    game = Game()
    size = 10
    game.reset(size)

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
            game.step(ActionEnum.ROTATE_LEFT)
        elif keys[pygame.K_d]:
            game.step(ActionEnum.ROTATE_RIGHT)
        elif keys[pygame.K_w]:
            game.step(ActionEnum.FORWARD)

        game.draw(screen)
        pygame.display.update()
        clock.tick(60)
