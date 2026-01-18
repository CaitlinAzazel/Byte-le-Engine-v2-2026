import os
import pygame as pyg

from game.common.enums import ObjectType
from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class VentBS(ByteSpriteFactory):
    """
    Vent bytesprite using Vent.png.

    SpriteSheet layout:
        Row 0 (top):     Vent
        Row 1 (bottom):  Vent Door
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
        # Use bottom row (vent door) if level designer wants this vent to look different
        if data.get('use_door_sprite', False):
            return spritesheets[1]

        # Default to top row (normal vent)
        return spritesheets[0]

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        return ByteSprite(
            screen,
            VentBS.VENT_PATH,
            2,                          # TWO rows: vent + door
            ObjectType.VENT.value,      # matches Adapter + game logs
            VentBS.update,
            colorkey=None               # use PNG alpha transparency
        )
