import pygame

from game.utils.vector import Vector


class InfoTemplate:
    def __init__(self, screen: pygame.Surface, topleft: Vector, size: Vector, font: str, color: str) -> None:
        self.screen: pygame.Surface = screen
        self.topleft: Vector = topleft
        self.size: Vector = size
        self.font: str = font
        self.color: str = color
        self.render_list: pygame.sprite.Group = pygame.sprite.Group()

    def recalc_animation(self, turn_log: dict) -> None:
        ...

    def render(self) -> None:
        self.render_list.draw(self.screen)
