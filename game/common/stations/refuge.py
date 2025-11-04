
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
    global_turns_outside = 5

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

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.vector = Vector(x, y)
        self.object_type: ObjectType = ObjectType.REFUGE
        Refuge.all_positions.add(self.vector)


    @override
    def to_json(self) -> dict:
        json = super().to_json()
        json['vector'] = self.vector
        json['occupied'] = self.global_occupied
        json['turns_inside'] = self.global_turns_inside
        return json

    @override
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.global_occupied = data['occupied']
        self.global_turns_inside = data['turns_inside']
        return self

    @override
    def can_occupy(self, game_object: GameObject) -> bool:
        return game_object.object_type == ObjectType.AVATAR and Refuge.global_turns_outside >= Refuge.MIN_TURNS_OUTSIDE

    @property
    def position(self) -> Vector:
        return self.vector

    @position.setter
    def position(self, new_position: Vector) -> None:
        self.vector = new_position
