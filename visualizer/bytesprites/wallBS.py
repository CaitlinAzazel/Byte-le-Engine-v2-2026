import os
import pygame as pyg

from game.common.enums import ObjectType
from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class WallBS(ByteSpriteFactory):
    """
    Static Wall bytesprite using Wall.png.
    """

    WALL_PATH = os.path.join(
        os.getcwd(),
        'visualizer/images/staticsprites/Wall.png'
    )

    @staticmethod
    def update(
        data: dict,
        layer: int,
        pos: Vector,
        spritesheets: list[list[pyg.Surface]]
    ) -> list[pyg.Surface]:
        # Use bottom row (shadow) if level designer wants this wall to look different
        if data.get('use_shadow_sprite', False):
            return spritesheets[1]
        return spritesheets[0]

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        return ByteSprite(
            screen,
            WallBS.WALL_PATH,
            2,                  # brick wall & shadow
            ObjectType.WALL.value,                  # object type (match Adapter)
            WallBS.update,
            colorkey=None       # use PNG alpha transparency
        )
