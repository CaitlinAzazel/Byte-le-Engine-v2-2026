import unittest
from game.fnaacm.bots.dumb_bot import DumbBot


class TestDumbBot(unittest.TestCase):
    def setUp(self):
        self.bot = DumbBot()

    def test_Movement_Unstunned(self):
        self.bot.player_seen = False
        repeat = 8
        while repeat > 0:
            DumbBot.movement(self.bot)
            print()
            repeat -= 1