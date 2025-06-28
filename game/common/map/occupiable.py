from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.items.item import Item
from typing import Self, Type
from game.common.avatar import Avatar
from game.utils.vector import Vector


class Occupiable(GameObject):
    """
    `Occupiable Class Notes:`

        This file acts as an Interface that other classes can inherit from to classify them as occupiable.

        Occupiable objects exist to encapsulate all objects that could be placed on the gameboard.

        These objects can only be occupied by GameObjects, so inheritance is important. The ``None`` value is
        acceptable for this too, showing that nothing is occupying the object.
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.object_type: ObjectType = ObjectType.OCCUPIABLE

    def to_json(self) -> dict:
        data: dict = super().to_json()
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        return self
