from game.common.enums import ObjectType
from game.common.map.occupiable import Occupiable
from game.utils.vector import Vector


class Refuge(Occupiable):
    MAX_TURNS_INSIDE = 10
    MIN_TURNS_OUTSIDE = 5

    all_positions: set[Vector] = set()

    """
        'Refuge Class Notes'

        The Refuge Station is a one-tile zone where the player can hide from the bots for a set number of turns.
        While within the Refuge, the following occurs:
            - the player's passive point generation each turn is halted
            - bots can no longer scan the player's location, reducing them to randomized pathfinding
            - a passive countdown starts that boots the player from the refuge upon hitting 0 to prevent excessive camping
            - boot countdown resets after a certain number of turns. all refuges share the same boot countdown

        The Refuge is intended to add a layer of strategy to the game, providing safety at the cost of valuable points
    """

    def __init__(self, x: int = 0, y: int = 0) -> None:
        super().__init__()
        self.vector = Vector(x, y)
        self.object_type: ObjectType = ObjectType.REFUGE
        Refuge.all_positions.add(self.vector)

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, Refuge) and \
            self.vector == value.vector

    @property
    def position(self) -> Vector:
        return self.vector

    @position.setter
    def position(self, new_position: Vector) -> None:
        if new_position != self.vector:
            Refuge.all_positions.remove(self.vector) # there should never be 2 refuges on the same tile so this is fine
            Refuge.all_positions.add(new_position)
        self.vector = new_position

    @property
    def is_closed(self) -> bool:
        ...
