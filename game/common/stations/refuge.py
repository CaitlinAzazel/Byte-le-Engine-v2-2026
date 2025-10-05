from operator import truediv

from game.common.botcommands.General_Bot_Commands import player
from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.items.item import Item
from typing import Self, Type
from game.common.avatar import Avatar
from game.common.map.occupiable import Occupiable
from game.utils.vector import Vector
from typing_extensions import override

class Refuge(Occupiable):
    __global_occupied = False
    __global_countdown_timer = 10
    __global_ejection_reset = 5

    """
        'Refuge Class Notes'

        The Refuge Station is a one-tile zone where the player can hide from the bots for a set number of turns.
        While within the Refuge, the following occurs:
            - the player's passive point generation each turn is halted
            - bots can no longer scan the player's location, reducing them to randomized pathfinding
            - a passive countdown starts that boots the player from the refuge upon hitting 0 to prevent excessive camping
            - boot countdown resets after a certain number of turns. all refuges share the same boot countdown

        The Refuge is intended to add a layer of strategy to the game, providing safety at the cost of valuable points

        The occupied/countdown_timer variables are meant to be global because their status can
                                        drastically change the state and operations of the entire game
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.vector = Vector(x, y)
        self.object_type: ObjectType = ObjectType.REFUGE


    @override
    def to_json(self) -> dict:
        json = super().to_json()
        json['vector'] = self.vector
        json['occupied'] = self.__global_occupied
        json['countdown_timer'] = self.__global_countdown_timer
        return json

    @override
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.__global_occupied = data['occupied']
        self.__global_countdown_timer = data['countdown_timer']
        return self

    @property
    def occupied(self) -> bool:
        return self.__global_occupied

    @occupied.setter
    def occupied(self, occupied: bool) -> None:
        self.__global_occupied = occupied

    @property
    def ejection_reset(self) -> int:
        return self.__global_ejection_reset

    @ejection_reset.setter
    def ejection_reset(self, value: int) -> None:
        self.__global_ejection_reset = value

    @property
    def countdown_timer(self) -> int:
        return self.__global_countdown_timer

    @countdown_timer.setter
    def countdown_timer(self, value: int) -> None:
        self.__global_countdown_timer = value

    @override
    def can_occupy(self, avatar: Avatar) -> bool:
        if self.ejection_reset >= 5:
            self.countdown_timer = 10
            return True
        else:
            return False

    def ejection(self, avatar: Avatar) -> None:
        avatar.position = avatar.position.add_y(1)

    def refuge_countdown(self, avatar: Avatar) -> None:
        if self.occupied:

            turns_remaining = self.countdown_timer
            self.countdown_timer = turns_remaining - 1
            self.ejection_reset = 0

            if self.countdown_timer <= 0:
                self.ejection(avatar)
                self.ejection_reset = 0
        else:
            self.ejection_reset += 1

    def refuge_tick(self, avatar: Avatar) -> None:
        if self.can_occupy(avatar) and avatar.position == self.vector:
            self.countdown_timer -= 1
        elif self.ejection_reset < 5:
            self.ejection_reset += 1

        self.refuge_countdown(avatar)

        """
                   # TO SET OCCUPIED:
                   We could do a coordinate system, where if the given Avatar matches the coordinates of the refuge, then occupied
                   is set to true. 
                   The issue is, grabbing coordinates from a subclass of game object requires other stuff. 

                   """

        """
                # Change Occupiable status and disallow players to be here. Make sure the player is ejected out as well.
                # With this being the case we need to ensure that there are no bots in the way, and that the method
                    # is compatible with different Refuge spaces across regions of the map
        """