import os
import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class DoorBS(ByteSpriteFactory):
    """
    Door ByteSprite Factory

    Sprite sheet row layout:
    0 -> CLOSED
    1 -> OPEN
    """

    @staticmethod
    def update(
        data: dict,
        layer: int,
        pos: Vector,
        spritesheets: list[list[pyg.Surface]]
    ) -> list[pyg.Surface]:

        # Treat missing data as CLOSED
        if data.get('open', False) or data.get('state') == 'open':
            return spritesheets[1]

        return spritesheets[0]

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        return ByteSprite(
            screen,
            os.path.join(
                os.getcwd(),
                'visualizer/images/spritesheets/Door.png'
            ),
            2,   # rows
            4,   # frames per row (even if static)
            DoorBS.update,
            colorkey=pyg.Color(255, 0, 255)
        )
