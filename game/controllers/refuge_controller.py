from typing import overload

from game.common.avatar import Avatar
from game.common.enums import BOT_OBJECT_TYPES, ActionType, ObjectType
from game.common.map.game_board import GameBoard
from game.common.map.occupiable import Occupiable
from game.common.player import Player
from game.common.stations.refuge import Refuge
from game.controllers.controller import Controller
from game.controllers.movement_controller import MovementController
from game.utils.vector import Vector


class RefugeController(Controller):
    def eject_avatar_from_refuge(self, avatar: Avatar, refuge_position: Vector, game_board: GameBoard) -> None:
        directions = [Vector(0,1), Vector(1, 0), Vector(0, -1), Vector(-1, 0)]

        # check if N, E, S, W tiles are occupiable, no bot
        for direction in directions:
            eject_to = refuge_position + direction
            if not game_board.is_occupiable(eject_to):
                continue

            objects = game_board.get_objects_from(eject_to)
            bot_found = False
            for obj in objects:
                # hack to avoid importing Bot
                if obj.object_type in BOT_OBJECT_TYPES:
                    bot_found = True
                    break
            if bot_found:
                continue

            tile = game_board.get_top(eject_to)
            if tile is None and not game_board.is_valid_coords(eject_to):
                continue
            elif isinstance(tile, Occupiable) and not tile.can_be_occupied_by(avatar):
                continue

            game_board.update_object_position(eject_to, avatar)
            return

        # pray it doesnt get here
        raise NotImplementedError()

    def handle_actions(self, action: ActionType,  client: Player, world: GameBoard) -> None:
        del action

        avatar: Avatar = client.avatar
        Refuge.global_occupied = False
        for pos in Refuge.all_positions:
            if pos == avatar.position:
                Refuge.global_occupied = True
                break

        if Refuge.global_occupied:
            Refuge.global_turns_inside += 1
            Refuge.global_turns_outside = 0
        else:
            Refuge.global_turns_outside += 1
            Refuge.global_turns_inside = 0

        if Refuge.global_turns_inside >= Refuge.MAX_TURNS_INSIDE:
            # avatar's position will be the same as whatever refuge they are in
            self.eject_avatar_from_refuge(avatar, avatar.position, world)
            Refuge.global_occupied = False
