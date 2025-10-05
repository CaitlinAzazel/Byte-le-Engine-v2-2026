import random

from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.controllers.master_controller import MasterController
from game.common.map.game_board import GameBoard
from game.controllers.movement_controller import MovementController


class DumbBot(GameObject):
    def __init__(self):
        super().__init__()
        self.vision = 1
        self.movement_controller: MovementController = MovementController()
        self.master_controller: MasterController = MasterController()
        self.game_board: GameBoard = GameBoard()
        self.player_seen : bool = False
        self.boosted : bool = False
        self.avatar: Avatar = Avatar()
        self.playerX: 0
        self.playerY: 0
        self.stun = False
        self.stun_counter = 0
        self.turn_counter = 0

    def movement(self):
        if not self.master_controller.game_over and not self.player_seen:
            if self.stun:
                self.stunned()
            else:
                movenum = random.randint(1,4)
                match movenum:
                    case 1:
                        moveUp(self)
                    case 2:
                        moveRight(self)
                    case 3:
                        moveDown(self)
                    case 4:
                        moveLeft(self)

    def player_seen_movement(self):
        if not self.master_controller.game_over and self.player_seen:
            if self.stun:
                self.stunned()
            else:
                if self.playerX > 0 and self.playerY == 0:
                    moveRight(self)
                elif self.playerX < 0 and self.playerY == 0:
                    moveLeft(self)
                elif self.playerX == 0 and self.playerY > 0:
                    moveDown(self)
                elif self.playerX == 0 and self.playerY < 0:
                    moveUp(self)
                elif self.playerX > 0 and self.playerY > 0:
                    if self.playerY > self.playerX:
                        moveDown(self)
                    else:
                        moveRight(self)
                elif self.playerX < 0 and self.playerY < 0:
                    if self.playerY < self.playerX:
                        moveUp(self)
                    else:
                        moveLeft(self)
                elif self.playerX > 0 and self.playerY < 0:
                    if abs(self.playerY) > self.playerX:
                        moveUp(self)
                    else:
                        moveRight(self)
                elif self.playerX < 0 and self.playerY > 0:
                    if self.playerY > abs(self.playerX):
                        moveDown(self)
                    else:
                        moveLeft(self)
                else:
                    self.movement()

    def player_scan(self):
        if not self.master_controller.game_over and not self.stun:
            if not self.boosted:
                self.player_seen, self.playerX, self.playerY = playerScan(self, 1)
            elif self.boosted:
                self.player_seen, self.playerX, self.playerY = playerScan(self, 2)

    def stunned(self):
        """do nothing"""
        self.stun_counter += 1
        if self.stun_counter == 5:
            self.stun = False
            self.stun_counter = 0
        return

    def action(self):
        self.turn_counter += 1

        if self.turn_counter % 2 != 0:
            return  # Only act every other turn

        self.player_scan()
        self.movement()
        self.player_seen_movement()