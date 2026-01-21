import unittest
from game.controllers.bot_movement_controller import BotMovementController
from game.fnaacm.bots.dumb_bot import DumbBot


class TestDumbBot(unittest.TestCase):
    def setUp(self):
        self.bot = DumbBot()

        self.bot_movement_controller = BotMovementController()

    def test_Movement_Unstunned(self):
        self.bot.player_seen = False
        repeat = 8
        while repeat > 0:
            self.bot_movement_controller.dumb_patrol()
            print()
            repeat -= 1
