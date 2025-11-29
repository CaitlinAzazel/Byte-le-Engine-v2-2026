import random

from game.fnaacm.bots.general_bot_commands import *
from game.common.map.game_board import GameBoard
from game.controllers.movement_controller import MovementController
from game.fnaacm.bots.bot import Bot

class DumbBot(Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vision = 1
        self.boosted : bool = False
        self.stun = False

    def __calc_next_move_patrol(self, gameboard : GameBoard, player: Player) -> list[ActionType]:
        return self.movement()

    def __calc_next_move_hunt(self, gameboard : GameBoard, player : Player) -> list[ActionType]:
        return self.player_seen_movement(player)

    def movement(self) -> list[ActionType]:
        if self.stun:
            self.stunned()
            return []
        return [random.choice([ActionType.MOVE_UP, ActionType.MOVE_RIGHT, ActionType.MOVE_DOWN, ActionType.MOVE_LEFT])]

    def player_seen_movement(self, player: Player) -> list[ActionType]:
        if self.stun:
            self.stunned()
            return []

        player_pos = player.avatar.position
        direction_to_player = (player_pos - self.position)
        playerX = direction_to_player.x
        playerY = direction_to_player.y
        if playerX > 0 and playerY == 0:
            return [ActionType.MOVE_RIGHT]
        elif playerX < 0 and playerY == 0:
            return [ActionType.MOVE_LEFT]
        elif playerX == 0 and playerY > 0:
            return [ActionType.MOVE_DOWN]
        elif playerX == 0 and playerY < 0:
            return [ActionType.MOVE_UP]
        elif playerX > 0 and playerY > 0:
            if playerY > playerX:
                return [ActionType.MOVE_DOWN]
            else:
                return [ActionType.MOVE_RIGHT]
        elif playerX < 0 and playerY < 0:
            if playerY < playerX:
                return [ActionType.MOVE_UP]
            else:
                return [ActionType.MOVE_LEFT]
        elif playerX > 0 and playerY < 0:
            if abs(playerY) > playerX:
                return [ActionType.MOVE_UP]
            else:
                return [ActionType.MOVE_RIGHT]
        elif playerX < 0 and playerY > 0:
            if playerY > abs(playerX):
                return [ActionType.MOVE_DOWN]
            else:
                return [ActionType.MOVE_LEFT]
        else:
            return self.movement()


    def action(self, player: Player):
        if self.can_see_player:
            self.__calc_next_move_hunt(self.game_board, player)
        else:
            self.__calc_next_move_patrol(self.game_board, player)
