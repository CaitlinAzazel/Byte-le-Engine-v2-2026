import random

from game.fnaacm.bots.general_bot_commands import *
from game.common.map.game_board import GameBoard
from game.fnaacm.bots.bot import Bot

class JumpBot(Bot):
    def __init__(self):
        super().__init__()
        self.vision = 2
        self.boosted : bool = False
        self.stun = False
        self.cooldown = 0

    def __calc_next_move_patrol(self, gameboard : GameBoard, player: Player) -> list[ActionType]:
        return self.movement()

    def __calc_next_move_hunt(self, gameboard : GameBoard, player : Player) -> list[ActionType]:
        return self.player_seen_movement(player)

    def movement(self) -> list[ActionType]:
        if self.stun:
            self.stunned()
            return []
        random1 = random.choice([ActionType.MOVE_UP, ActionType.MOVE_DOWN])
        random2 = random.choice([ActionType.MOVE_RIGHT, ActionType.MOVE_LEFT])
        return [random1, random2]

    def player_seen_movement(self, player: Player) -> list[ActionType]:
        if self.stun:
            self.stunned()
            return []

        player_pos = player.avatar.position
        direction_to_player = (player_pos - self.position)
        playerX = direction_to_player.x
        playerY = direction_to_player.y
        if self.boosted:
            if self.cooldown != 0:
                self.cooldown -= 1
                if playerX > 0 and playerY == 0:
                    randomvar = random.choice([ActionType.MOVE_UP, ActionType.MOVE_DOWN])
                    return [randomvar, ActionType.MOVE_RIGHT]
                elif playerX < 0 and playerY == 0:
                    randomvar = random.choice([ActionType.MOVE_UP, ActionType.MOVE_DOWN])
                    return [randomvar, ActionType.MOVE_LEFT]
                elif playerX == 0 and playerY > 0:
                    randomvar = random.choice([ActionType.MOVE_LEFT, ActionType.MOVE_RIGHT])
                    return [ActionType.MOVE_DOWN, randomvar]
                elif playerX == 0 and playerY < 0:
                    randomvar = random.choice([ActionType.MOVE_LEFT, ActionType.MOVE_RIGHT])
                    return [ActionType.MOVE_UP, randomvar]
                elif playerX > 0 and playerY > 0:
                    return [ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT]
                elif playerX < 0 and playerY < 0:
                    return [ActionType.MOVE_UP, ActionType.MOVE_LEFT]
                elif playerX > 0 and playerY < 0:
                    return [ActionType.MOVE_UP, ActionType.MOVE_RIGHT]
                elif playerX < 0 and playerY > 0:
                    return [ActionType.MOVE_DOWN, ActionType.MOVE_LEFT]
                else:
                    return self.movement()
            elif self.cooldown == 0:
                self.cooldown = random.randint(1,3)
                if playerX > 0 and playerY == 0:
                    return [ActionType.MOVE_RIGHT, ActionType.MOVE_RIGHT]
                elif playerX < 0 and playerY == 0:
                    return [ActionType.MOVE_LEFT, ActionType.MOVE_LEFT]
                elif playerX == 0 and playerY > 0:
                    return [ActionType.MOVE_DOWN, ActionType.MOVE_DOWN]
                elif playerX == 0 and playerY < 0:
                    return [ActionType.MOVE_UP, ActionType.MOVE_UP]
                elif playerX > 0 and playerY > 0:
                    return [ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT, ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT]
                elif playerX < 0 and playerY < 0:
                    return [ActionType.MOVE_UP, ActionType.MOVE_LEFT, ActionType.MOVE_UP, ActionType.MOVE_LEFT]
                elif playerX > 0 and playerY < 0:
                    return [ActionType.MOVE_UP, ActionType.MOVE_RIGHT, ActionType.MOVE_UP, ActionType.MOVE_RIGHT]
                elif playerX < 0 and playerY > 0:
                    return [ActionType.MOVE_DOWN, ActionType.MOVE_LEFT, ActionType.MOVE_DOWN, ActionType.MOVE_LEFT]
                else:
                    return self.movement()
            else:
                self.movement()
        elif not self.boosted:
            if self.cooldown != 0:
                self.cooldown -= 1
            if playerX > 0 and playerY == 0:
                randomvar = random.choice([ActionType.MOVE_UP, ActionType.MOVE_DOWN])
                return [randomvar, ActionType.MOVE_RIGHT]
            elif playerX < 0 and playerY == 0:
                randomvar = random.choice([ActionType.MOVE_UP, ActionType.MOVE_DOWN])
                return [randomvar, ActionType.MOVE_LEFT]
            elif playerX == 0 and playerY > 0:
                randomvar = random.choice([ActionType.MOVE_LEFT, ActionType.MOVE_RIGHT])
                return [ActionType.MOVE_DOWN, randomvar]
            elif playerX == 0 and playerY < 0:
                randomvar = random.choice([ActionType.MOVE_LEFT, ActionType.MOVE_RIGHT])
                return [ActionType.MOVE_UP, randomvar]
            elif playerX > 0 and playerY > 0:
                return [ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT]
            elif playerX < 0 and playerY < 0:
                return [ActionType.MOVE_UP, ActionType.MOVE_LEFT]
            elif playerX > 0 and playerY < 0:
                return [ActionType.MOVE_UP, ActionType.MOVE_RIGHT]
            elif playerX < 0 and playerY > 0:
                return [ActionType.MOVE_DOWN, ActionType.MOVE_LEFT]
            else:
                return self.movement()

    def action(self):
        if self.can_see_player:
            self.__calc_next_move_hunt(self.game_board, player)
        else:
            self.__calc_next_move_patrol(self.game_board, player)
