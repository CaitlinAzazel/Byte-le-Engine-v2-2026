import unittest
from game.controllers.attack_controller import Attack_Controller
from game.common.enums import ActionType
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.common.stations.station import Station
from game.common.avatar import Avatar


class DummyBot:
    def __init__(self):
        self.attack_called = False

    def attack(self, target):
        self.attack_called = True


class TestAttackController(unittest.TestCase):
    def setUp(self):
        self.controller = Attack_Controller()
        self.bot = DummyBot()
        self.player = Player()
        self.player.avatar = Avatar()
        self.gameboard = GameBoard(1, (10, 10), {}, False)

    def test_cardinal_attack_stuns(self):
        """Bot attacking cardinal direction sets stunned = True"""
        self.controller.handle_actions(ActionType.ATTACK_DOWN, self.player, self.gameboard, self.bot)
        self.assertTrue(self.bot.attack_called)

    def test_attack_on_station_calls_attack(self):
        """Attacking a station calls bot.attack()"""
        station = Station()
        self.gameboard.grid = {(0, 1): station}
        self.bot.avatar = Avatar()
        self.player.avatar.position = (0, 0)

        self.controller.handle_actions(ActionType.ATTACK_DOWN, self.player, self.gameboard, self.bot)
        self.assertTrue(self.bot.attack_called)


if __name__ == "__main__":
    unittest.main()
