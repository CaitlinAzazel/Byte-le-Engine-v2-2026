import os
import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class scrapBS(ByteSpriteFactory):
    """
    Static scrap bytesprite using Scrap.png.
    """
    SCRAP_PATH = os.path.join(os.getcwd(), 'visualizer/images/staticsprites/Scrap.png')

    @staticmethod
    def update(data: dict, layer: int, pos: Vector, spritesheets: list[list[pyg.Surface]]) -> list[pyg.Surface]:
        # Always return the first surface; static vent
        return spritesheets[0]

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        # Pass path to ByteSprite; it will load internally
        return ByteSprite(
            screen,
            scrapBS.SCRAP_PATH,  # positional argument
            2,                 # layer
            8,                 # object type
            scrapBS.update,     # update function
            colorkey=pyg.Color(0, 0, 0, 0)  # transparency
        )
