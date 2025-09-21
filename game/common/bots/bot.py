from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.fnaacm.cooldown import Cooldown
from game.utils.vector import Vector


DEFAULT_STUN_DURATION = 5

class Bot(GameObject):
    def __init__(self, stun_duration : int = DEFAULT_STUN_DURATION, start_position : Vector = Vector() ):
        super().__init__()
        self.boosted : bool = False
        self.stunned : Cooldown = Cooldown(stun_duration)
        self.position : Vector = start_position

    def calc_next_pos(self, gameboard : GameBoard, avatar_position : Vector = Vector() ) -> Vector:
        pass

    def can_attack(self, in_refuge: bool, in_vent: bool, avatar_pos: Vector) -> bool:
        """
        Can the bot attack the player?
        -> Call in the botAttack controller
        -> Pass in requisite information to check if the player CAN be hit
        -> if so, hit the player
        -> hit command controlled by FNAACM player class
        -> isInVent, isInRefuge, otherwise hit
        """
        return not (in_refuge or in_vent)


