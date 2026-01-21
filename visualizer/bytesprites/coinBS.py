import os
import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from game.common.enums import ObjectType
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class CoinBS(ByteSpriteFactory):
    """
    Static Coin bytesprite using Coin.png.
    """

    COIN_PATH = os.path.join(
        os.getcwd(),
        'visualizer/images/staticsprites/Coin.png'
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
            CoinBS.COIN_PATH,
            2,
            ObjectType.COIN.value,                  # object type (match Adapter)
            CoinBS.update,
            colorkey=None       # use PNG alpha transparency
        )
