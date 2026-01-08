import os
import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class BoosterBotBS(ByteSpriteFactory):
    """
    BoosterBot ByteSprite Factory

    Sprite sheet row layout:
    0 -> ON
    1 -> OFF
    """

    @staticmethod
    def update(
        data: dict,
        layer: int,
        pos: Vector,
        spritesheets: list[list[pyg.Surface]]
    ) -> list[pyg.Surface]:

        # Treat missing data as OFF
        if data.get('on', False) or data.get('state') == 'on':
            return spritesheets[0]

        return spritesheets[1]

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        return ByteSprite(
            screen,
            os.path.join(
                os.getcwd(),
                'visualizer/images/spritesheets/BoosterBot.png'
            ),
            2,   # rows
            4,   # frames per row
            BoosterBotBS.update,
            colorkey=pyg.Color(255, 0, 255)
        )
