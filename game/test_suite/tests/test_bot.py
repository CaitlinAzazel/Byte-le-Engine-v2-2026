import unittest
from game.common.avatar import Avatar
from game.common.stations.refuge import Refuge
from game.fnaacm.bots import bot
from game.fnaacm.bots.bot import DEFAULT_VISION_RADIUS, Bot
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
            player_pos: [self.player.avatar],
            bot_pos: [self.bot],
        }
        game_board = GameBoard(0, Vector(1, 2), locations)
        game_board.generate_map()
        self.assertTrue(self.bot.can_attack(game_board, self.player))

    def test_cannot_attack_into_vent(self):
        player_pos: Vector = self.player.avatar.position
        bot_pos: Vector = player_pos + Vector(0, 1)
        locations: dict[Vector, list[GameObject]] = {
            player_pos: [Vent(), self.player.avatar],
            bot_pos: [self.bot],
        }
        game_board = GameBoard(0, Vector(1, 2), locations)
        game_board.generate_map()
        self.assertFalse(self.bot.can_attack(game_board, self.player))

    def test_cannot_attack_into_refuge(self):
        player_pos: Vector = self.player.avatar.position
        bot_pos: Vector = player_pos + Vector(0, 1)
        locations: dict[Vector, list[GameObject]] = {
            player_pos: [Refuge(player_pos.x, player_pos.y), self.player.avatar],
            bot_pos: [self.bot],
        }
        game_board = GameBoard(0, Vector(1, 2), locations)
        game_board.generate_map()
        Refuge.refuge_tick(self.player.avatar, game_board)
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
        player_pos: Vector = self.player.avatar.position
        bot_pos: Vector = player_pos + Vector(DEFAULT_VISION_RADIUS+1)
        locations: dict[Vector, list[GameObject]] = {
            player_pos: [self.player],
            bot_pos: [self.bot],
        }
        game_board = GameBoard(0, Vector(DEFAULT_VISION_RADIUS+1, 1))
        game_board.generate_map()
        self.assertFalse(self.bot.can_see_player(game_board, self.player))

    def test_cannot_see_player_in_vent(self):
        locations: dict[Vector, list[GameObject]] = \
            {
                Vector(1,1): [self.bot],
                Vector(2,2): [self.vent, self.player.avatar]
            }

        game_board = GameBoard(0, Vector(3,3), locations, True)
        game_board.generate_map()
        self.assertFalse(self.bot.can_see_player(game_board, self.player))

    def test_cannot_see_player_behind_wall(self):
        game_board = GameBoard()
        # TODO: set up map where wall is between player and bot
        self.assertFalse(self.bot.can_see_player(game_board, self.player))



