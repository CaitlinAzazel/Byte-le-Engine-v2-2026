import random

from General_Bot_Commands import *
from game.common.avatar import Avatar
from game.controllers.master_controller import MasterController
from game.common.map.game_board import GameBoard
from game.utils.vector import Vector


class Dumb_Bot:
    def __init__(self):
        super().__init__()
        self.vision = 1
        self.movement_controller: MovementController = MovementController()
        self.master_controller: MasterController = MasterController()
        self.game_board: GameBoard = GameBoard()
        self.player_seen : bool = False
        self.boosted : bool = False
        self.avatar: Avatar = Avatar()

    def movement(self):
        while not self.master_controller.game_over and not self.player_seen:
            moveNum = random.randint(1,4)
            match moveNum:
                case 1:
                    moveUp(self)
                case 2:
                    moveRight(self)
                case 3:
                    moveDown(self)
                case 4:
                    moveLeft(self)

    def playerSeenMovement(self):
        while not self.master_controller.game_over and self.player_seen:
            bot_pos: Vector = Vector(self.avatar.position.x, self.avatar.position.y)
            if self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(0,1)), Avatar):
                moveDown(self)
            elif self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(0,-1)), Avatar):
                moveUp(self)
            elif self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(1,0)), Avatar):
                moveRight(self)
            elif self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-1,0)), Avatar):
                moveLeft(self)
            elif self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(1,1)), Avatar):
                moveNum = random.randint(1,2)
                if moveNum == 1:
                    moveDown(self)
                elif moveNum == 2:
                    moveRight(self)
                else:
                    self.movement()
            elif self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-1,1)), Avatar):
                moveNum = random.randint(1,2)
                if moveNum == 1:
                    moveDown(self)
                elif moveNum == 2:
                    moveLeft(self)
                else:
                    self.movement()
            elif self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(1,-1)), Avatar):
                moveNum = random.randint(1,2)
                if moveNum == 1:
                    moveUp(self)
                elif moveNum == 2:
                    moveRight(self)
                else:
                    self.movement()
            elif self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-1,-1)), Avatar):
                moveNum = random.randint(1,2)
                if moveNum == 1:
                    moveUp(self)
                elif moveNum == 2:
                    moveLeft(self)
                else:
                    self.movement()
            else:
                self.movement()

    def playerScan(self):
        while not self.master_controller.game_over:
            bot_pos: Vector = Vector(self.avatar.position.x, self.avatar.position.y)
            if not self.boosted:
                if not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(0,1)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(0,-1)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(1,0)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-1,0)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(1,1)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-1,1)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(1,-1)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-1,-1)), Avatar) :
                    self.player_seen = False
                else:
                    self.player_seen = True
            elif self.boosted:
                if not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(0,1)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(0,-1)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(1,0)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-1,0)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(1,1)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-1,1)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(1,-1)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-1,-1)), Avatar)\
                        and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-2,-2)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-1,-2)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(0,-2)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(1,-2)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(2,-2)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(2,-1)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(2,0)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(2,1)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(2,2)), Avatar) \
                        and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(1,2)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(0,2)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-1, 2)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-2, 2)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-2, 1)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-2, 0)), Avatar) and not self.game_board.get_objects_from(Vector(bot_pos.add_to_vector(-2, -1)), Avatar):
                    self.player_seen = False
                else:
                    self.player_seen = True