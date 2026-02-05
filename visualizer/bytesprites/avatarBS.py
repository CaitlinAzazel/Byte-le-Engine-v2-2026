import os
import pygame as pyg

from game.common.enums import ObjectType
from visualizer.bytesprites.bytesprite import ByteSprite
from game.utils.vector import Vector
from visualizer.bytesprites.bytesprite_factory import ByteSpriteFactory


class AvatarBS(ByteSpriteFactory):
    """
    Avatar ByteSprite Factory

    Sprite sheet row layout:
    0 -> Moving Down
    1 -> Moving Right
    2 -> Moving Left
    3 -> Moving Up
    4 -> Hurt / Attacked
    """

    @staticmethod
    def update(
        data: dict,
        layer: int,
        pos: Vector,
        spritesheets: list[list[pyg.Surface]]
    ) -> list[pyg.Surface]:

        # --- Hurt state overrides everything ---
        if data.get('state') == 'hurt' or data.get('hurt', False):
            return spritesheets[4]

        direction = data.get('direction', 'down')

        if direction == 'down':
            return spritesheets[0]
        elif direction == 'right':
            return spritesheets[1]
        elif direction == 'left':
            return spritesheets[2]
        elif direction == 'up':
            return spritesheets[3]

        # Fallback (idle / unknown)
        return spritesheets[0]

    @staticmethod
    def create_bytesprite(screen: pyg.Surface) -> ByteSprite:
        return ByteSprite(
            screen,
            os.path.join(os.getcwd(), 'visualizer/images/spritesheets/Player.png'),
            5,
            ObjectType.AVATAR.value,
            AvatarBS.update,
            colorkey=pyg.Color(255, 0, 255)
        )


