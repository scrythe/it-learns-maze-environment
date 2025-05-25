import pygame
from .actions import ActionEnum
import math


class Player:
    def __init__(self, radius, rotation_speed, movement_speed):
        self.radius = radius
        self.rotation_speed = rotation_speed
        self.movement_speed = movement_speed
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        pygame.draw.circle(self.image, "Red", (self.radius, self.radius), self.radius)
        self.image.set_colorkey("Black")
        self.rect = self.image.get_frect()

    def reset(self):
        self.rect.topleft = (120, 120)
        self.angle = 0

    def step(self, action: ActionEnum):
        match action:
            case ActionEnum.ROTATE_LEFT:
                self.angle -= self.rotation_speed
                if self.angle < 0:
                    self.angle += 2 * math.pi
            case ActionEnum.ROTATE_RIGHT:
                self.angle += self.rotation_speed
                if self.angle > 2 * math.pi:
                    self.angle -= 2 * math.pi
            case ActionEnum.FORWARD:
                direction_x = math.cos(self.angle) * self.movement_speed
                direction_y = math.sin(self.angle) * self.movement_speed
                self.rect.x += direction_x
                self.rect.y += direction_y

    def draw(self, screen: pygame.Surface):
        end_line_x = self.rect.centerx + math.cos(self.angle) * 20
        end_line_y = self.rect.centery + math.sin(self.angle) * 20
        pygame.draw.line(screen, "Blue", self.rect.center, (end_line_x, end_line_y), 5)
        screen.blit(self.image, self.rect)
