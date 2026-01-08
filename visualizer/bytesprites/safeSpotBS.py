import os
import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory
from game.common.enums import ObjectType


class SafeSpotBS(ByteSpriteFactory):
    """
    Static safe spot bytesprite using SafeSpot.png.
    """

    SAFESPOT_PATH = os.path.join(
        os.getcwd(),
        'visualizer/images/staticsprites/SafeSpot.png'
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
            SafeSpotBS.SAFESPOT_PATH,
            1,                          # one row (static)
            ObjectType.SAFE_SPOT.value, # must match Adapter + logs
            SafeSpotBS.update,
            colorkey=None               # use PNG alpha transparency
        )
