from abc import abstractmethod

from game.common.avatar import Avatar
from game.common.enums import ActionType
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.map.game_object_container import GameObjectContainer
from game.common.map.occupiable import Occupiable
from game.common.player import Player
from game.common.stations.refuge import Refuge
from game.utils.vector import Vector


DEFAULT_STUN_DURATION = 5
DEFAULT_VISION_RADIUS = 1

class Bot(GameObject):
    def __init__(self, stun_duration : int = DEFAULT_STUN_DURATION, start_position : Vector = Vector(), vision_radius: int = DEFAULT_VISION_RADIUS):
        super().__init__()
        self.boosted : bool = False
        self.is_stunned : bool = False
        self.position : Vector = start_position
        self.vision_radius: int = vision_radius
        self.boosted_vision_radius: int = vision_radius * 2
        self.can_see_into_vent: bool = False
        self.stun_counter: int = 0
        self.has_attacked: bool = False

    def _calc_next_move_hunt(self, gameboard : GameBoard, player: Player) -> list[ActionType]:
        return []

    def _calc_next_move_patrol(self, gameboard : GameBoard, player: Player) -> list[ActionType]:
        return []

    def _is_tile_open(self, tile_data: GameObjectContainer) -> bool:
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
            if isinstance(game_object, Occupiable) and game_object.can_be_occupied_by(self):
                continue

            return False

        return True

    def can_see_player(self, game_board: GameBoard, player: Player) -> bool:
        distance_to_player: int = self.position.distance(player.avatar.position)
        vision_radius = self.boosted_vision_radius if self.boosted else self.vision_radius
        in_vision: bool = self.in_vision_radius(player.avatar.position)
        if Refuge.global_occupied:
            return False

        if not in_vision:
            return False

        positions_between = GameBoard.get_positions_overlapped_by_line(player.avatar.position, self.position)
        for position in positions_between:
            tile_objects = game_board.get(position)
            if not self._is_tile_open(tile_objects):
                return False


    """
    The position input into this method will almost entirely be used for Avatar. 
    However, this method can also be used to compute whether objects like a generator, door, or vent
    are within a vision radius
    """
    def in_vision_radius(self, pos: Vector) -> bool:
        if self.boosted:
            top_left = Vector(self.position.x - self.boosted_vision_radius, self.position.y - self.boosted_vision_radius)
            bottom_right = Vector(self.position.x + self.boosted_vision_radius, self.position.y + self.boosted_vision_radius)
        else:
            top_left = Vector(self.position.x - self.vision_radius, self.position.y - self.vision_radius)
            bottom_right = Vector(self.position.x + self.vision_radius, self.position.y + self.vision_radius)

        if top_left.x <= pos.x <= bottom_right.x and top_left.y <= pos.y <= bottom_right.y:
            return True
        return False


    def calc_next_move(self, gameboard : GameBoard, player : Player) -> list[ActionType]:
        """
        returns actions that the bot should take to get to wherever it wants to go (typically player vector)
        """
        if self.can_see_player(gameboard, player):
            return self._calc_next_move_hunt(gameboard, player)
        return self._calc_next_move_patrol(gameboard, player)

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


    def attack(self, target):
        """
        Perform an attack on the target Avatar.
        Tests expect:
        - bot.has_attacked becomes True
        - target receives the attack via target.receive_attack(bot)
        """
        if target is None:
            return

        # Avatar defines receive_attack()
        if hasattr(target, "receive_attack"):
            target.receive_attack(self)

        # Bot stunned after hitting the player
        self.is_stunned = True
        self.stun_counter = 0

        self.has_attacked = True
