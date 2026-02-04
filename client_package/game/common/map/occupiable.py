from game.common.enums import ObjectType
from game.common.game_object import GameObject


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

    def can_be_occupied_by(self, game_object: GameObject) -> bool:
        ...
