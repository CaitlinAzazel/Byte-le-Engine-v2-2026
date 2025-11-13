import unittest

from game.common.enums import ActionType
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.stations.refuge import Refuge
from game.controllers.bot_movement_controller import BotMovementController
from game.fnaacm.bots.bot import Bot
from game.utils.vector import Vector
from game.fnaacm.map.vent import Vent


class TestBotMovementController(unittest.TestCase):
    def setUp(self) -> None:
        self.bot_movement_controller = BotMovementController()
        self.bot = Bot(start_position=Vector(2,2)) 

        refuge_pos = Vector(0,2)
        self.locations: dict[Vector, list[GameObject]] = {
            self.bot.position: [self.bot],
            Vector(2, 0): [Vent()],
            refuge_pos: [Refuge(refuge_pos.x, refuge_pos.y)],
        }
        self.game_board = GameBoard(0, Vector(4, 4), self.locations, False)
        self.game_board.generate_map()

    def test_move_all_directions(self):
        self.bot_movement_controller.handle_actions(ActionType.MOVE_UP, self.bot, self.game_board)
        self.assertEqual(self.bot.position, Vector(2, 1))

    def test_move_down(self):
        self.bot_movement_controller.handle_actions(ActionType.MOVE_DOWN, self.bot, self.game_board)
        self.assertEqual(self.bot.position, Vector(2, 3))

    def test_move_left(self):
        self.bot_movement_controller.handle_actions(ActionType.MOVE_LEFT, self.bot, self.game_board)
        self.assertEqual(self.bot.position, Vector(1, 2))

    def test_move_right(self):
        self.bot_movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.bot, self.game_board)
        self.assertEqual(self.bot.position, Vector(3, 2))

    def test_move_right_invalid_coordinate(self):
        self.bot_movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.bot, self.game_board)
        self.bot_movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.bot, self.game_board)
        self.assertEqual(self.bot.position, Vector(3, 2))

    def test_cannot_move_into_vent(self):
        for _ in range(2):
            self.bot_movement_controller.handle_actions(ActionType.MOVE_UP, self.bot, self.game_board)
        self.assertEqual(self.bot.position, Vector(2, 1))

    def test_cannot_move_into_refuge(self):
        for _ in range(2):
            self.bot_movement_controller.handle_actions(ActionType.MOVE_LEFT, self.bot, self.game_board)
        self.assertEqual(self.bot.position, Vector(1, 2))

