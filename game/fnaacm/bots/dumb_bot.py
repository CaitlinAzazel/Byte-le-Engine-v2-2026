import random
from typing import override

from game.fnaacm.bots.general_bot_commands import *
# from game.common.map.game_board import GameBoard
# from game.controllers.movement_controller import MovementController
from game.fnaacm.bots.bot import Bot

class DumbBot(Bot):
    def __init__(self):
        super().__init__()
        self.vision = 1
        self.boosted : bool = False
        self.stun = False

    # @override
    # def _calc_next_move_patrol(self, gameboard : GameBoard, player: Player) -> list[ActionType]:
    #     if self.stun:
    #         self.stunned()
    #         return []
    #     return [random.choice([ActionType.MOVE_UP, ActionType.MOVE_RIGHT, ActionType.MOVE_DOWN, ActionType.MOVE_LEFT])]
    #
    # @override
    # def _calc_next_move_hunt(self, gameboard : GameBoard, player : Player) -> list[ActionType]:
    #     if self.stun:
    #         self.stunned()
    #         return []
    #
    #     player_pos = player.avatar.position
    #     direction_to_player = (player_pos - self.position)
    #     playerX = direction_to_player.x
    #     playerY = direction_to_player.y
    #     if playerX > 0 and playerY == 0:
    #         return [ActionType.MOVE_RIGHT]
    #     elif playerX < 0 and playerY == 0:
    #         return [ActionType.MOVE_LEFT]
    #     elif playerX == 0 and playerY > 0:
    #         return [ActionType.MOVE_DOWN]
    #     elif playerX == 0 and playerY < 0:
    #         return [ActionType.MOVE_UP]
    #     elif playerX > 0 and playerY > 0:
    #         if playerY > playerX:
    #             return [ActionType.MOVE_DOWN]
    #         else:
    #             return [ActionType.MOVE_RIGHT]
    #     elif playerX < 0 and playerY < 0:
    #         if playerY < playerX:
    #             return [ActionType.MOVE_UP]
    #         else:
    #             return [ActionType.MOVE_LEFT]
    #     elif playerX > 0 and playerY < 0:
    #         if abs(playerY) > playerX:
    #             return [ActionType.MOVE_UP]
    #         else:
    #             return [ActionType.MOVE_RIGHT]
    #     elif playerX < 0 and playerY > 0:
    #         if playerY > abs(playerX):
    #             return [ActionType.MOVE_DOWN]
    #         else:
    #             return [ActionType.MOVE_LEFT]
    #     else:
    #         return self._calc_next_move_patrol(gameboard, player)
