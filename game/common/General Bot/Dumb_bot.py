import random

from General_Bot_Commands import *
from game.common.avatar import Avatar
from game.controllers.master_controller import MasterController
from game.common.map.game_board import GameBoard


class DumbBot:
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

    def movement(self):
        while not self.master_controller.game_over and not self.player_seen:
            if self.stun:
                self.stunned(self)
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
        while not self.master_controller.game_over and self.player_seen:
            if self.stun:
                self.stunned(self)
            else:
                if self.playerX > 0 and self.playerY > 0:
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
        while not self.master_controller.game_over and not self.stun:
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
