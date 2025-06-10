import random

from General_Bot_Commands import *
from game.common.avatar import Avatar
from game.controllers.master_controller import MasterController
from game.common.map.game_board import GameBoard

class JumpBot:
    def __init__(self):
        super().__init__()
        self.vision = 2
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
        self.cooldown = 0

    def movement(self):
        while not self.master_controller.game_over and not self.player_seen:
            if self.stun:
                self.stunned()
            else:
                movenum = random.randint(1,4)
                match movenum:
                    case 1:
                        moveUp(self)
                        moveRight(self)
                    case 2:
                        moveDown(self)
                        moveRight(self)
                    case 3:
                        moveDown(self)
                        moveLeft(self)
                    case 4:
                        moveUp(self)
                        moveLeft(self)

    def player_seen_movement(self):
        while not self.master_controller.game_over and self.player_seen:
            if self.stun:
                self.stunned()
            if self.boosted:
                if self.cooldown != 0:
                    self.cooldown -= 1
                    moveNum = random.randint(1,2)
                    if self.playerX > 0 and self.playerY == 0:
                        match moveNum:
                            case 1:
                                moveUp(self)
                                moveRight(self)
                            case 2:
                                moveDown(self)
                                moveRight(self)
                    elif self.playerX < 0 and self.playerY == 0:
                        match moveNum:
                            case 1:
                                moveUp(self)
                                moveLeft(self)
                            case 2:
                                moveDown(self)
                                moveLeft(self)
                    elif self.playerX == 0 and self.playerY > 0:
                        match moveNum:
                            case 1:
                                moveDown(self)
                                moveLeft(self)
                            case 2:
                                moveDown(self)
                                moveRight(self)
                    elif self.playerX == 0 and self.playerY < 0:
                        match moveNum:
                            case 1:
                                moveUp(self)
                                moveLeft(self)
                            case 2:
                                moveUp(self)
                                moveRight(self)
                    elif self.playerX > 0 and self.playerY > 0:
                        moveDown(self)
                        moveRight(self)
                    elif self.playerX < 0 and self.playerY < 0:
                        moveUp(self)
                        moveLeft(self)
                    elif self.playerX > 0 and self.playerY < 0:
                        moveUp(self)
                        moveRight(self)
                    elif self.playerX < 0 and self.playerY > 0:
                        moveDown(self)
                        moveLeft(self)
                    else:
                        self.movement()
                elif self.cooldown == 0:
                    self.cooldown = random.randint(1,3)
                    if self.playerX > 0 and self.playerY == 0:
                        moveRight(self)
                        moveRight(self)
                    elif self.playerX < 0 and self.playerY == 0:
                        moveLeft(self)
                        moveLeft(self)
                    elif self.playerX == 0 and self.playerY > 0:
                        moveDown(self)
                        moveDown(self)
                    elif self.playerX == 0 and self.playerY < 0:
                        moveUp(self)
                        moveUp(self)
                    elif self.playerX > 0 and self.playerY > 0:
                        moveDown(self)
                        moveRight(self)
                        moveDown(self)
                        moveRight(self)
                    elif self.playerX < 0 and self.playerY < 0:
                        moveUp(self)
                        moveLeft(self)
                        moveUp(self)
                        moveLeft(self)
                    elif self.playerX > 0 and self.playerY < 0:
                        moveUp(self)
                        moveRight(self)
                        moveUp(self)
                        moveRight(self)
                    elif self.playerX < 0 and self.playerY > 0:
                        moveDown(self)
                        moveLeft(self)
                        moveDown(self)
                        moveLeft(self)
                    else:
                        self.movement()
                else:
                    self.movement()
            elif not self.boosted:
                if self.cooldown != 0:
                    self.cooldown -= 1
                moveNum = random.randint(1, 2)
                if self.playerX > 0 and self.playerY == 0:
                    match moveNum:
                        case 1:
                            moveUp(self)
                            moveRight(self)
                        case 2:
                            moveDown(self)
                            moveRight(self)
                elif self.playerX < 0 and self.playerY == 0:
                    match moveNum:
                        case 1:
                            moveUp(self)
                            moveLeft(self)
                        case 2:
                            moveDown(self)
                            moveLeft(self)
                elif self.playerX == 0 and self.playerY > 0:
                    match moveNum:
                        case 1:
                            moveDown(self)
                            moveLeft(self)
                        case 2:
                            moveDown(self)
                            moveRight(self)
                elif self.playerX == 0 and self.playerY < 0:
                    match moveNum:
                        case 1:
                            moveUp(self)
                            moveLeft(self)
                        case 2:
                            moveUp(self)
                            moveRight(self)
                elif self.playerX > 0 and self.playerY > 0:
                    moveDown(self)
                    moveRight(self)
                elif self.playerX < 0 and self.playerY < 0:
                    moveUp(self)
                    moveLeft(self)
                elif self.playerX > 0 and self.playerY < 0:
                    moveUp(self)
                    moveRight(self)
                elif self.playerX < 0 and self.playerY > 0:
                    moveDown(self)
                    moveLeft(self)
                else:
                    self.movement()


    def player_scan(self):
        while not self.master_controller.game_over and not self.stun:
            if not self.boosted:
                self.player_seen, self.playerX, self.playerY = playerScan(self, 2)
            elif self.boosted:
                self.player_seen, self.playerX, self.playerY = playerScan(self, 4)

    def stunned(self):
        """do nothing"""
        self.stun_counter += 1
        if self.stun_counter == 5:
            self.stun = False
            self.stun_counter = 0

    def action(self):
        self.player_scan()
        self.movement()
        self.player_seen_movement()