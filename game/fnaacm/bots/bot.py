from abc import abstractmethod
from typing import Self

from game.common.avatar import Avatar
from game.common.enums import ActionType
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.map.game_object_container import GameObjectContainer
from game.common.map.occupiable import Occupiable
from game.common.player import Player
from game.common.stations.refuge import Refuge
from game.utils.ldtk_json import EntityInstance
from game.utils.vector import Vector


DEFAULT_STUN_DURATION = 5
DEFAULT_VISION_RADIUS = 1

class Bot(GameObject):
    class LDtkFieldIdentifiers:
        PATROL_ROUTE = 'patrol_route'

    def __init__(self, stun_duration : int = DEFAULT_STUN_DURATION, start_position : Vector = Vector(), vision_radius: int = DEFAULT_VISION_RADIUS, patrol_route: list[Vector] = []):
        super().__init__()
        self.boosted : bool = False
        self.is_stunned : bool = False
        self.position : Vector = start_position
        self.vision_radius: int = vision_radius
        self.boosted_vision_radius: int = vision_radius * 2
        self.can_see_into_vent: bool = False
        self.stun_counter: int = 0
        self.patrol_routes: list[Vector] = patrol_route
        self.current_patrol_waypoint_index: int = 0

    @classmethod
    def from_ldtk_entity(cls, entity: EntityInstance) -> Self:
        position: Vector = Vector(entity.grid[0], entity.grid[1])
        patrol_route = []
        for field in entity.field_instances:
            match field.identifier:
                case Bot.LDtkFieldIdentifiers.PATROL_ROUTE:
                    for x in field.value:
                        print(x)
        return cls(start_position=position, patrol_route=patrol_route)

    @abstractmethod
    def __calc_next_move_hunt(self, gameboard : GameBoard, player: Player) -> list[ActionType]:
        pass

    @abstractmethod
    def __calc_next_move_patrol(self, gameboard : GameBoard, player: Player) -> list[ActionType]:
        pass

    def __is_tile_open(self, tile_data: GameObjectContainer) -> bool:
        """
        determines if a tile "blocks" this bot's line of sight or not

        override in Bot subclasses if more complex behavior is needed
        """
        for game_object in tile_data:
            # "see through" other bots and players
            if isinstance(game_object, Bot):
                continue
            if isinstance(game_object, Avatar):
                continue

            # crawler can occupy vents, so it can see into them; other bots cannot
            # unless something like windows are added, this will work
            if isinstance(game_object, Occupiable) and not game_object.can_be_occupied_by(self):
                return False

        return True

    def can_see_player(self, game_board: GameBoard, player: Player) -> bool:
        distance_to_player: int = self.position.distance(player.avatar.position)
        vision_radius = self.boosted_vision_radius if self.boosted else self.vision_radius
        in_vision: bool = distance_to_player <= vision_radius
        if not in_vision:
            return False

        positions_between = GameBoard.get_positions_overlapped_by_line(self.position, player.avatar.position)
        for position in positions_between:
            tile_objects = game_board.get(position)
            if not self.__is_tile_open(tile_objects):
                return False

        return not Refuge.global_occupied

    def calc_next_move(self, gameboard : GameBoard, player : Player) -> list[ActionType]:
        """
        returns actions that the bot should take to get to wherever it wants to go (typically player vector)
        """
        if self.can_see_player(gameboard, player):
            return self.__calc_next_move_hunt(gameboard, player)
        return self.__calc_next_move_patrol(gameboard, player)

    def can_attack(self, game_board: GameBoard, player: Player) -> bool:
        # distance check is just a shortcut for checking up/down/left/right
        return self.can_see_player(game_board, player) and self.position.distance(player.avatar.position) <= 1

    def boosting(self, boost):
        self.boosted = boost

    def stunned(self):
        """do nothing"""
        self.stun_counter += 1
        if self.stun_counter == 5:
            self.is_stunned = False
            self.stun_counter = 0
        return

    def can_act(self, turn: int) -> bool:
        return turn % 2 == 0
