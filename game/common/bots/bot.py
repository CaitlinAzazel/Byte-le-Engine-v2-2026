from abc import abstractmethod
from game.common.avatar import Avatar
from game.common.enums import ActionType
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.fnaacm.cooldown import Cooldown
from game.fnaacm.fnaacm_player import FNAACMPlayer
from game.utils.vector import Vector


DEFAULT_STUN_DURATION = 5
DEFAULT_VISION_RADIUS = 1

class Bot(GameObject):
    def __init__(self, stun_duration : int = DEFAULT_STUN_DURATION, start_position : Vector = Vector(), vision_radius: int = DEFAULT_VISION_RADIUS):
        super().__init__()
        self.boosted : bool = False
        self.stunned : Cooldown = Cooldown(stun_duration)
        self.position : Vector = start_position
        self.vision_radius: int = vision_radius

    @abstractmethod
    def __calc_next_move_hunt(self, gameboard : GameBoard, player: FNAACMPlayer) -> list[ActionType]:
        pass

    @abstractmethod
    def __calc_next_move_patrol(self, gameboard : GameBoard, player: FNAACMPlayer) -> list[ActionType]:
        pass

    def can_see_player(self, game_board: GameBoard, player: FNAACMPlayer) -> bool:
        # TODO: actually check if player is behind wall
        is_behind_wall: bool = False
        distance_to_player: int = self.position.distance(player.avatar.position)
        in_vision: bool = distance_to_player <= self.vision_radius
        return not is_behind_wall and in_vision and not player.in_refuge()

    def calc_next_move(self, gameboard : GameBoard, player : FNAACMPlayer ) -> list[ActionType]:
        """
        returns actions that the bot should take to get to wherever it wants to go (typically player vector)
        """
        if self.can_see_player(gameboard, player):
            return self.__calc_next_move_hunt(gameboard, player)
        return self.__calc_next_move_patrol(gameboard, player)

    def can_attack(self, game_board: GameBoard, player: FNAACMPlayer) -> bool:
        """
        HOW TO USE THIS METHOD IN THE BOT ATTACK CONTROLLER:
        Can the bot attack the player?
        -> Call in the botAttack controller
        -> Pass in requisite information to check if the player CAN be hit
        -> if so, hit the player
        -> hit command controlled by FNAACM player class
        -> is_in_vent, is_in_refuge, otherwise hit
        """
        # should there be max attack radius?
        return self.can_see_player(game_board, player) and not (player.in_refuge() or player.in_vent(game_board))


