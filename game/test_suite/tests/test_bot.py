import unittest
from game.common.bots.bot import Bot
from game.common.fnaacm_player import FNAACMPlayer
from game.common.map.game_board import GameBoard


class TestBot(unittest.TestCase):
    def setUp(self) -> None:
        self.player = FNAACMPlayer()
        self.bot = Bot()

    """
    `calc_next_move` should be tested by respective bots since
    they all have unique movement patterns
    """

    # can the bot attack in "optimal" conditions?
    def test_can_attack(self):
        game_board = GameBoard()
        # TODO: set up map where player and bot are standing next to each other,
        # no special conditions
        self.assertTrue(self.bot.can_attack(game_board, self.player))

    def test_cannot_attack_into_vent(self):
        game_board = GameBoard()
        # TODO: set up map where player and bot are standing next to each other,
        # player is in a vent
        self.assertFalse(self.bot.can_attack(game_board, self.player))

    def test_cannot_attack_into_refuge(self):
        game_board = GameBoard()
        # TODO: set up map where player and bot are standing next to each other,
        # player is in a refuge
        self.assertFalse(self.bot.can_attack(game_board, self.player))

    def test_cannot_see_past_vision_radius(self):
        game_board = GameBoard()
        # TODO: set up map where player is outside of vision radius
        self.assertFalse(self.bot.can_see_player(game_board, self.player))

    def test_cannot_see_player_in_vent(self):
        game_board = GameBoard()
        # TODO: set up map where player is in vent, bot is outside
        self.assertFalse(self.bot.can_see_player(game_board, self.player))

    def test_cannot_see_player_behind_wall(self):
        game_board = GameBoard()
        # TODO: set up map where wall is between player and bot
        self.assertFalse(self.bot.can_see_player(game_board, self.player))



