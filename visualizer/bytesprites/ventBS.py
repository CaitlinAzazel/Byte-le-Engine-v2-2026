import os
import pygame as pyg

from game.common.enums import ObjectType
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
        if data['use_door_sprite']:
            return spritesheets[1]
        return spritesheets[0]

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        return ByteSprite(
            screen,
            VentBS.VENT_PATH,
            1,                  # one row
            ObjectType.VENT.value,                  # object type (match Adapter)
            VentBS.update,
            colorkey=None       # alpha transparency
        )
