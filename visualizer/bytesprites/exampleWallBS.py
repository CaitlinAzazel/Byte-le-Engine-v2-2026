import os

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class WallBytespriteFactoryExample(ByteSpriteFactory):
    """
    This class is used to demonstrate an example of the Wall Bytesprite. It demonstrates how any class inheriting
    from ByteSpriteFactory must implement the `update()` and `create_bytesprite()` static methods. These methods may
    have unique implementations based on how the sprites are meant to look and interact with other objects in the game.
    """
    @staticmethod
    def update(data: dict, layer: int, pos: Vector, spritesheets: list[list[pyg.Surface]]) -> list[pyg.Surface]:
        """
        This method implementation simply returns the first spritesheet in the list of given spritesheets. Examining the
        `ExampleWallSS.png` file, it is clear that there is only one spritesheet, so that is all this method needs to
        do.
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
        :return: a ByteSprite object
        """
        return ByteSprite(screen, os.path.join(os.getcwd(), 'visualizer/images/spritesheets/ExampleWallSS.png'), 1,
                          8, WallBytespriteFactoryExample.update)
