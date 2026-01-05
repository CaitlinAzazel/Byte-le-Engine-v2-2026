import os
import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class VentBS(ByteSpriteFactory):
    """
    Static vent bytesprite using Vent.png.
    """

    VENT_PATH = os.path.join(
        os.getcwd(),
        'visualizer/images/staticsprites/Vent.png'
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
            VentBS.VENT_PATH,
            1,                  # one row
            8,                  # object type (match Adapter)
            VentBS.update,
            colorkey=None       # alpha transparency
        )
