from game.common.avatar import Avatar
from game.common.enums import ActionType
from game.common.player import Player
from game.controllers.movement_controller import MovementController
from game.common.map.game_board import GameBoard
from game.utils.vector import Vector

player = Player()
gameboard = GameBoard()

def moveLeft(bot):
    MovementController.handle_actions(bot, ActionType(4), player, gameboard)

def moveUp(bot):
    MovementController.handle_actions(bot, ActionType(2), player, gameboard)

def moveRight(bot):
    MovementController.handle_actions(bot, ActionType(5), player, gameboard)

def moveDown(bot):
    MovementController.handle_actions(bot, ActionType(3), player, gameboard)

def playerScan(bot, radius):
        bot_pos: Vector = Vector(bot.avatar.position.x, bot.avatar.position.y)
        i = 1
        while(i <= radius):
            j = 0
            while(j <= radius):
                if (not bot.game_board.get_objects_from(Vector(bot_pos.add_to_vector(j, i)),Avatar) and not bot.game_board.get_objects_from(Vector(bot_pos.add_to_vector(j, -i)), Avatar) and not bot.game_board.get_objects_from(Vector(bot_pos.add_to_vector(i, j)), Avatar) and not bot.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-i, j)), Avatar) and not bot.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-i, -j)), Avatar) and not bot.game_board.get_objects_from(Vector(bot_pos.add_to_vector(i, -j)), Avatar) and not bot.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-j, i)), Avatar)):
                    j += 1
                else:
                    if bot.game_board.get_objects_from(Vector(bot_pos.add_to_vector(j, i)),Avatar):
                        return True, j, i
                    if bot.game_board.get_objects_from(Vector(bot_pos.add_to_vector(j, -i)),Avatar):
                        return True, j, -i
                    if bot.game_board.get_objects_from(Vector(bot_pos.add_to_vector(i, j)),Avatar):
                        return True, i, j
                    if bot.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-i, j)),Avatar):
                        return True, -i, j
                    if bot.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-i, -j)),Avatar):
                        return True, -i, -j
                    if bot.game_board.get_objects_from(Vector(bot_pos.add_to_vector(i, -j)),Avatar):
                        return True, i, -j
                    if bot.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-j, i)),Avatar):
                        return True, -j, i
            i += 1
        return False, 0, 0

def stun():
    Dumb_bot.stun = True
    Support_bot.stun = True
    Jumper_Bot.stun = True
    Crawler_Bot.stun = True
    IAN_Bot.stun = True
