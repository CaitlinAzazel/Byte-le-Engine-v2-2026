import os
import pygame as pyg

class GameFrame:
    BORDER_PATH = os.path.join(
        os.getcwd(),
        'visualizer/images/staticsprites/Border.png'
    )

    GAME_WIDTH = 1280
    GAME_HEIGHT = 720

    def __init__(self, screen: pyg.Surface):
        self.screen = screen
        self.image = pyg.image.load(self.BORDER_PATH).convert_alpha()

        # Safety: ensure correct size
        self.image = pyg.transform.smoothscale(
            self.image,
            (self.GAME_WIDTH, self.GAME_HEIGHT)
        )

    def get_rect(self) -> pyg.Rect:
        return self.image.get_rect(
            center=self.screen.get_rect().center
        )

    def render(self) -> None:
        self.screen.blit(self.image, self.get_rect())
