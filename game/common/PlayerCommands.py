from game.common.enums import ActionType
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.movement_controller import MovementController
from game.common.botcommands.General_Bot_Commands import stun

class PlayerCommands():
    def __init__(self):
        self.player = Player()
        self.gameboard = GameBoard()
        self.movement_controller = MovementController()
        self.health = 3

    def moveLeft(self):
        MovementController.handle_actions(self.movement_controller, ActionType(4), self.player, self.gameboard)

    def moveUp(self):
        MovementController.handle_actions(self.movement_controller, ActionType(2), self.player, self.gameboard)

    def moveRight(self):
        MovementController.handle_actions(self.movement_controller, ActionType(5), self.player, self.gameboard)

    def moveDown(self):
        MovementController.handle_actions(self.movement_controller, ActionType(3), self.player, self.gameboard)

    def whenHit(self):
        stun()
        self.health -= 1