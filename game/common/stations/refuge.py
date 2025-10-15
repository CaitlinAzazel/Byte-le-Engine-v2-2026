
from game.common.enums import ObjectType
from typing import Self, Type
from game.common.avatar import Avatar
from game.common.map.game_board import GameBoard
from game.common.map.occupiable import Occupiable
from game.controllers.movement_controller import MovementController
from game.utils.vector import Vector
from typing_extensions import override

class Refuge(Occupiable):
    global_occupied = False
    global_turns_inside = 0
    global_turns_outside = 5

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
    def can_occupy(self, avatar: Avatar) -> bool:
        return Refuge.global_turns_outside >= 5

    @staticmethod
    def ejection(avatar: Avatar, refuge_position: Vector, game_board: GameBoard) -> None:
        directions = [Vector(0,1), Vector(1, 0), Vector(0, -1), Vector(-1, 0)]

        # check if N, E, S, W tiles are occupiable, no bot
        for direction in directions:
            eject_to = refuge_position + direction
            if not game_board.is_occupiable(eject_to):
                continue

            objects = game_board.get_objects_from(eject_to)
            bot_found = False
            for object in objects:
                # FIXME: import Bot once merged
                if (isinstance(object, Bot)):
                    bot_found = True
                    break
            if bot_found:
                continue

            tile = game_board.get_top( eject_to )
            if isinstance(tile, Occupiable) and not tile.can_occupy(avatar):
                continue

            MovementController.update_avatar_position(eject_to, avatar, game_board)
        
        # pray it doesnt get here

    @staticmethod
    def refuge_countdown(avatar: Avatar) -> None:
        Refuge.global_turns_inside += 1
        if Refuge.global_turns_inside >= 10:
            Refuge.ejection(avatar)
            Refuge.global_turns_outside = 0

    @staticmethod
    def refuge_tick(avatar: Avatar) -> None:
        if Refuge.global_occupied:
            Refuge.refuge_countdown(avatar)
        else:
            Refuge.global_turns_outside += 1



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