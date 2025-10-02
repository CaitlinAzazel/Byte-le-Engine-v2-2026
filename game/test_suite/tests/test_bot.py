import unittest
from game.common.avatar import Avatar
from game.common.bots.bot import Bot
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.fnaacm.map.vent import Vent
from game.fnaacm.fnaacm_player import FNAACMPlayer
from game.utils.vector import Vector


class TestBot(unittest.TestCase):
    def setUp(self) -> None:
        self.avatar = Avatar(position=Vector())
        self.player = FNAACMPlayer(avatar=self.avatar)
        self.bot = Bot()

        self.vent = Vent()
        self.vent_pos = Vector()

    """
    `calc_next_move` should be tested by respective bots since
    they all have unique movement patterns
    """

    # can the bot ATTACK in "optimal" conditions?
    def test_can_attack(self):
        player_pos: Vector = self.player.avatar.position
        bot_pos: Vector = player_pos + Vector(0, 1)
        # no special conditions
        locations: dict[Vector, list[GameObject]] = {
            player_pos: [self.player],
            bot_pos: [self.bot],
        }
        game_board = GameBoard(0, Vector(1, 2), locations)
        game_board.generate_map()
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


    # can the bot SEE in "optimal" conditions?
    def test_can_see(self):
        player_pos: Vector = self.player.avatar.position
        bot_pos: Vector = player_pos + Vector(0, 1)
        # no special conditions
        locations: dict[Vector, list[GameObject]] = {
            player_pos: [self.player],
            bot_pos: [self.bot],
        }
        game_board = GameBoard(0, Vector(1, 2), locations)
        game_board.generate_map()
        self.assertTrue(self.bot.can_see_player(game_board, self.player))

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



