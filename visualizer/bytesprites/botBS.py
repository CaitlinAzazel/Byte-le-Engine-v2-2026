import os
import pygame as pyg

from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class MovingBotBS(ByteSpriteFactory):
    """
    Shared ByteSprite factory for moving bots:
    - IanBot
    - JumperBot
    - DumbBot
    - CrawlerBot

    Sprite sheet row layout:
    0 -> Moving Down
    1 -> Moving Right
    2 -> Moving Left
    3 -> Moving Up
    """

    @staticmethod
    def update(
        data: dict,
        layer: int,
        pos: Vector,
        spritesheets: list[list[pyg.Surface]]
    ) -> list[pyg.Surface]:

        direction = data.get('direction', 'down')

        if direction == 'down':
            return spritesheets[0]
        elif direction == 'right':
            return spritesheets[1]
        elif direction == 'left':
            return spritesheets[2]
        elif direction == 'up':
            return spritesheets[3]

        return spritesheets[0]

    @staticmethod
    def create_bytesprite(
        screen: pyg.Surface,
        spritesheet_name: str
    ) -> ByteSprite:
        """
        spritesheet_name allows each bot to have its own image
        while sharing animation logic.
        """
        return ByteSprite(
            screen,
            os.path.join(
                os.getcwd(),
                f'visualizer/images/spritesheets/{spritesheet_name}'
            ),
            4,   # rows
            4,   # frames per row
            MovingBotBS.update,
            colorkey=pyg.Color(255, 0, 255)
        )
