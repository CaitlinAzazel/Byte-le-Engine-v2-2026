import os
import pygame as pyg
from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory
from game.common.enums import ObjectType

class BatteryBS(ByteSpriteFactory):
    """
    Static battery bytesprite using Battery.png.
    """
    BATTERY_PATH = os.path.join(os.getcwd(), 'visualizer/images/staticsprites/Battery.png')

    @staticmethod
    def update(data: dict, layer: int, pos: Vector, spritesheets: list[list[pyg.Surface]]) -> list[pyg.Surface]:
        if data['state'] != 'idle':
            return spritesheets[1]
        return spritesheets[0]

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        return ByteSprite(
            screen,
            BatteryBS.BATTERY_PATH,
            2,
            ObjectType.BATTERY_SPAWNER.value,
            BatteryBS.update,
            colorkey=pyg.Color(0,0,0,0)
        )
