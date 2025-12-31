# wallBS.py
import os
import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class WallBS(ByteSpriteFactory):
    """
    Static wall bytesprite using Wall.png.
    """
    WALL_PATH = os.path.join(os.getcwd(), 'visualizer/images/staticsprites/Wall.png')

    @staticmethod
    def update(data: dict, layer: int, pos: Vector, spritesheets: list[list[pyg.Surface]]) -> list[pyg.Surface]:
        # Always return the first surface; static wall
        return spritesheets[0]

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        # Pass path to ByteSprite; it will load internally
        return ByteSprite(
            screen,
            WallBS.WALL_PATH,  # positional argument
            2,                 # layer
            8,                 # object type
            WallBS.update,     # update function
            colorkey=pyg.Color(0, 0, 0, 0)  # transparency
        )
