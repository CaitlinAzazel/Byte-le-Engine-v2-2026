import unittest
from game.controllers.bot_movement_controller import BotMovementController
from game.utils.vector import Vector
from game.common.map.game_board import GameBoard
from game.fnaacm.map.vent import Vent
from game.fnaacm.bots.dumb_bot import DumbBot
from game.common.avatar import Avatar
from game.common.player import Player
from game.common.enums import ActionType

class TestDumbBot(unittest.TestCase):
    def setUp(self):
           # Create board and player
        self.board = GameBoard(map_size=Vector(5, 5))
        self.board.generate_map()
        self.player_avatar = Avatar(position=Vector(2, 2))
        self.player = Player(avatar=self.player_avatar)

        # Create bot at top-left
        self.bot = DumbBot()
        self.bot.position = Vector(0, 0)

        self.bot_movement_controller = BotMovementController()

    def test_Movement_Unstunned(self):
        pass

