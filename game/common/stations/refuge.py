
from typing import Self
from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.map.occupiable import Occupiable
from game.utils.vector import Vector
from typing_extensions import override



class Refuge(Occupiable):
    MAX_TURNS_INSIDE = 10
    MIN_TURNS_OUTSIDE = 5

    global_occupied = False
    global_turns_inside = 0
    global_turns_outside = MIN_TURNS_OUTSIDE

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

        The occupied/turns_inside variables are meant to be global because their status can
                                        drastically change the state and operations of the entire game
    """

    def __init__(self, x: int = 0, y: int = 0) -> None:
        super().__init__()
        self.vector = Vector(x, y)
        self.object_type: ObjectType = ObjectType.REFUGE
        Refuge.all_positions.add(self.vector)

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, Refuge) and \
            self.vector == value.vector

    @staticmethod
    def reset_global_state():
        Refuge.global_occupied = False
        Refuge.global_turns_inside = 0
        Refuge.global_turns_outside = Refuge.MIN_TURNS_OUTSIDE

    @override
    def to_json(self) -> dict:
        json = super().to_json()
        json['vector'] = self.vector.to_json()
        json['occupied'] = self.global_occupied
        json['turns_inside'] = self.global_turns_inside
        json['is_closed'] = self.is_closed
        return json

    @override
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.global_occupied = data['occupied']
        self.global_turns_inside = data['turns_inside']
        self.vector = Vector().from_json(data['vector'])
        return self

    @override
    def can_occupy(self, game_object: GameObject) -> bool:
        if game_object.object_type != ObjectType.AVATAR:
            return False
        if self.is_closed:
            return False
        return True

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
        return not Refuge.global_occupied and Refuge.global_turns_outside < Refuge.MIN_TURNS_OUTSIDE
