import os
import pygame as pyg

from game.common.enums import ObjectType
from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class TileBS(ByteSpriteFactory):
    """
    Static Tile bytesprite using Tile.png.
    """

    TILE_PATH = os.path.join(
        os.getcwd(),
        'visualizer/images/staticsprites/Tile.png'
    )

    @staticmethod
    def update(
        data: dict,
        layer: int,
        pos: Vector,
        spritesheets: list[list[pyg.Surface]]
    ) -> list[pyg.Surface]:
        # Static sprite: always use first row
        return spritesheets[0]

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        return ByteSprite(
            screen,
            TileBS.TILE_PATH,
            1,                  # one row for static tile
            ObjectType.TILE.value,                  # object type (match Adapter)
            TileBS.update,
            colorkey=None       # use PNG alpha for transparency
        )
