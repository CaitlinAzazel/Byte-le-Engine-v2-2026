from game.common.enums import ActionType
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.movement_controller import MovementController
from game.common.botcommands.General_Bot_Commands import stun, player
from game.controllers.master_controller import MasterController
from game.common.avatar import Avatar
from game.controllers.interact_controller import InteractController

class PlayerCommands():
    def __init__(self):
        self.player = Player()
        self.gameboard = GameBoard()
        self.movement_controller = MovementController()
        self.health = 3
        self.tempPower = 0
        self.pointsTotal = 0
        self.inSafeZone = False

    def moveLeft(self):
        MovementController.handle_actions(self.movement_controller, ActionType(4), self.player, self.gameboard)

    def moveUp(self):
        MovementController.handle_actions(self.movement_controller, ActionType(2), self.player, self.gameboard)

    def moveRight(self):
        MovementController.handle_actions(self.movement_controller, ActionType(5), self.player, self.gameboard)

    def moveDown(self):
        MovementController.handle_actions(self.movement_controller, ActionType(3), self.player, self.gameboard)

    def __whenHit(self):
        stun()
        self.health -= 1
        self.tempPower = player.power(self) - 50
        if self.tempPower < 0:
            self.tempPower = 0
        player.power(self, self.tempPower)
        if self.health <= 0:
            MasterController.game_over = True

    def addPoint(self):
        if not self.inSafeZone:
            self.pointsTotal += 1
        else:
            self.pointsTotal += 0

    def action(self):
        self.addPoint()