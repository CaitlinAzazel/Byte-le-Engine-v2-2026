import os

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class TileBytespriteFactoryExample(ByteSpriteFactory):
    """
    This class is used to demonstrate an example of the Tile Bytesprite. It demonstrates how any class inheriting
    from ByteSpriteFactory must implement the `update()` and `create_bytesprite()` static methods. These methods may
    have unique implementations based on how the sprites are meant to look and interact with other objects in the game.
    """
    @staticmethod
    def update(data: dict, layer: int, pos: Vector, spritesheets: list[list[pyg.Surface]]) -> list[pyg.Surface]:
        """
        This implementation of the update method is different from the exampleWallBS.py file. In this method, the
        data dictionary is used. The `data` is a dict representing a Tile object in JSON notation.

        For this unique implementation, an if statement is used to check if something is occupying the Tile object.
        If true, the second spritesheet is used. If false, the first spritesheet is used.

        Examining the ExampleTileSS.png, it is apparent that the first spritesheet shows a Tile with an animation with
        only the pink color. However, the second spritesheet (the one used if something occupies that tile) has a unique
        animation that is blue instead.
        :param data:
        :param layer:
        :param pos:
        :param spritesheets:
        :return:
        """
        return spritesheets[0]

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        """
        This method takes a screen from Pygame.Surface. That screen is then passed in as a parameter into the
        returned Bytesprite object.
        :param screen:
        :return:
        """
        return ByteSprite(screen, os.path.join(os.getcwd(), 'visualizer/images/spritesheets/ExampleTileSS.png'), 2,
                          7, TileBytespriteFactoryExample.update)
