
import unittest

from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.common.stations.refuge import Refuge
from game.controllers.bot_vision_controller import BotVisionController
from game.controllers.refuge_controller import RefugeController
from game.fnaacm.bots.bot import Bot
from game.utils.vector import Vector
from game.fnaacm.map.vent import Vent
from game.common.map.wall import Wall


class TestBotMovementController(unittest.TestCase):
    def setUp(self) -> None:
        self.avatar = Avatar(position=Vector())
        self.player = Player(avatar=self.avatar)
        self.bot = Bot()
        self.vision_controller = BotVisionController()

        self.vent = Vent()
        self.vent_pos = Vector()
        self.refuge_controller = RefugeController()
        Refuge.reset_global_state()

    # can the bot SEE in "optimal" conditions?
    def test_can_see(self):
        self.bot.position = self.avatar.position + Vector(0, 1)
        # no special conditions
        locations: dict[Vector, list[GameObject]] = {
            self.avatar.position: [self.avatar],
            self.bot.position: [self.bot],
        }
        game_board = GameBoard(0, Vector(1, 2), locations)
        game_board.generate_map()
        self.vision_controller.handle_actions(self.avatar, self.bot, game_board)
        self.assertTrue(self.bot.can_see_player)

    def test_cannot_see_past_vision_radius(self):
        self.avatar.position = Vector(0, 0)
        self.bot.position = Vector(Bot.DEFAULT_VISION_RADIUS+1)
        locations: dict[Vector, list[GameObject]] = {
            self.avatar.position: [self.avatar],
            self.bot.position: [self.bot],
        }
        game_board = GameBoard(0, Vector(Bot.DEFAULT_VISION_RADIUS+1, 1), locations)
        game_board.generate_map()
        self.vision_controller.handle_actions(self.avatar, self.bot, game_board)
        self.assertFalse(self.bot.can_see_player)

    def test_cannot_see_player_in_vent(self):
        locations: dict[Vector, list[GameObject]] = \
            {
                Vector(1,1): [self.bot],
                Vector(2,2): [self.vent, self.player.avatar]
            }

        game_board = GameBoard(0, Vector(3,3), locations, True)
        game_board.generate_map()
        self.vision_controller.handle_actions(self.avatar, self.bot, game_board)
        self.assertFalse(self.bot.can_see_player)

    def test_cannot_see_player_behind_wall(self):
        self.avatar.position = Vector(0, 0)
        self.bot.position = Vector(Bot.DEFAULT_VISION_RADIUS+1)
        locations: dict[Vector, list[GameObject]] = {
            self.avatar.position: [self.avatar],
            Vector(1,0): [Wall()],
            self.bot.position: [self.bot],
        }
        game_board = GameBoard(0, Vector(3, 1), locations)
        game_board.generate_map()
        self.vision_controller.handle_actions(self.avatar, self.bot, game_board)
        self.assertFalse(self.bot.can_see_player)



