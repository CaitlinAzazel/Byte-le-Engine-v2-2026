import os
import random

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class AvatarBytespriteFactoryExample(ByteSpriteFactory):
    """
    `Avatar Bytesprite Factory Example Notes`:

        This is a factory class that will produce Bytesprite objects of the Avatar.
    """
    @staticmethod
    def update(data: dict, layer: int, pos: Vector, spritesheets: list[list[pyg.Surface]]) -> list[pyg.Surface]:
        """
        This method will select which spritesheet to select from the ``ExampleSpritesheet.png`` file. For example,
        the first if statement will return the second row of sprites in the image if conditions are met.
        :param data:
        :param layer:
        :param pos:
        :param spritesheets:
        :return: list[pyg.Surface]
        """

        # Logic for selecting active animation
        if data['inventory'][data['held_index']] is not None:
            return spritesheets[1]
        elif random.randint(1, 6) == 6:
            return spritesheets[2]
        elif random.randint(1, 4) == 4:
            return spritesheets[3]
        else:
            return spritesheets[0]

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        """
        This file will return a new ByteSprite object that is to be displayed on the screen.
        :param screen: ByteSprite
        :return:
        """
        return ByteSprite(screen, os.path.join(os.getcwd(), 'visualizer/images/spritesheets/ExampleSpritesheet.png'), 4,
                          4, AvatarBytespriteFactoryExample.update, pyg.Color("#FBBBAD"))
