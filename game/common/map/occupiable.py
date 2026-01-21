from warnings import deprecated
from game.common.enums import ObjectType
from game.common.game_object import GameObject
from typing import Self


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

    @deprecated("If accessing, use `can_be_occupied_by` instead as it is more descriptive. If overriding, go ahead.")
    def can_occupy(self, game_object: GameObject) -> bool:
        return True

    # TODO: replace all uses of can_occupy with this better named method
    def can_be_occupied_by(self, game_object: GameObject) -> bool:
        return self.can_occupy(game_object)
