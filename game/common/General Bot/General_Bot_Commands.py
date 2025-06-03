from game.common.enums import ActionType
from game.common.player import Player
from game.controllers.movement_controller import MovementController
from game.common.map.game_board import GameBoard

player = Player()
def moveLeft(bot):
    MovementController.handle_actions(bot, ActionType(4), player, GameBoard)
def moveUp(bot):
    MovementController.handle_actions(bot, ActionType(2), player, GameBoard)
def moveRight(bot):
    MovementController.handle_actions(bot, ActionType(5), player, GameBoard)
def moveDown(bot):
    MovementController.handle_actions(bot, ActionType(3), player, GameBoard)