import os
import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class GeneratorBS(ByteSpriteFactory):
    """
    Static Generator bytesprite using Generator.png.
    """

    GENERATOR_PATH = os.path.join(
        os.getcwd(),
        'visualizer/images/staticsprites/Generator.png'
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
            GeneratorBS.GENERATOR_PATH,
            1,                  # one row for static sprite
            8,                  # object type (match Adapter)
            GeneratorBS.update,
            colorkey=None       # use PNG alpha transparency
        )
