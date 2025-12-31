# tileBS.py
import os
import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class TileBS(ByteSpriteFactory):
    """
    Static tile bytesprite using Tile.png.
    """
    TILE_PATH = os.path.join(os.getcwd(), 'visualizer/images/staticsprites/Tile.png')

    @staticmethod
    def update(data: dict, layer: int, pos: Vector, spritesheets: list[list[pyg.Surface]]) -> list[pyg.Surface]:
        # Always return the first surface; static tile
        return spritesheets[0]

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        # Only pass path to ByteSprite; it will load internally
        return ByteSprite(
            screen,
            TileBS.TILE_PATH,
            1,
            7,
            TileBS.update,
            colorkey=pyg.Color(0, 0, 0, 0)
        )

