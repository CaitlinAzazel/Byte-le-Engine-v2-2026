import os
import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class ScrapBS(ByteSpriteFactory):
    """
    Static scrap / coin bytesprite using Scrap.png.
    """

    SCRAP_PATH = os.path.join(
        os.getcwd(),
        'visualizer/images/staticsprites/Scrap.png'
    )

    @staticmethod
    def update(
        data: dict,
        layer: int,
        pos: Vector,
        spritesheets: list[list[pyg.Surface]]
    ) -> list[pyg.Surface]:
        if data['state'] != 'idle':
            return spritesheets[1]
        return spritesheets[0]

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        return ByteSprite(
            screen,
            ScrapBS.SCRAP_PATH,
            2,
            8,                  # object type (match Adapter)
            ScrapBS.update,
            colorkey=None       # use alpha transparency
        )
