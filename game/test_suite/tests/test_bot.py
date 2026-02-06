import unittest
from game.common.avatar import Avatar
from game.common.enums import ActionType
from game.common.map.wall import Wall
from game.common.player import Player
from game.common.stations.refuge import Refuge
from game.controllers.bot_vision_controller import BotVisionController
from game.controllers.refuge_controller import RefugeController
from game.fnaacm.bots.bot import Bot
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.fnaacm.map.vent import Vent
from game.utils.vector import Vector


class TestBot(unittest.TestCase):
    def setUp(self) -> None:
        self.avatar = Avatar(position=Vector())
        self.player = Player(avatar=self.avatar)
        self.bot = Bot()

        self.vent = Vent()
        self.vent_pos = Vector()
        self.refuge_controller = RefugeController()
        Refuge.reset_global_state()
        self.bot_vision_controller = BotVisionController()
        Bot.reset_global_state()

    """
    `calc_next_move` should be tested by respective bots since
    they all have unique movement patterns
    """

    # can the bot ATTACK in "optimal" conditions?
    def test_can_attack(self):
        player_pos: Vector = self.avatar.position
        bot_pos: Vector = player_pos + Vector(0, 1)
        # no special conditions
        locations: dict[Vector, list[GameObject]] = {
            player_pos: [self.avatar],
            bot_pos: [self.bot],
        }
        game_board = GameBoard(0, Vector(1, 2), locations)
        game_board.generate_map()
        self.bot_vision_controller.handle_actions(self.avatar, self.bot, game_board)
        self.assertTrue(self.bot.can_attack(self.avatar))

    def test_cannot_attack_into_vent(self):
        player_pos: Vector = self.avatar.position
        bot_pos: Vector = player_pos + Vector(0, 1)
        locations: dict[Vector, list[GameObject]] = {
            player_pos: [Vent(), self.avatar],
            bot_pos: [self.bot],
        }
        game_board = GameBoard(0, Vector(1, 2), locations)
        game_board.generate_map()
        self.bot_vision_controller.handle_actions(self.avatar, self.bot, game_board)
        self.assertFalse(self.bot.can_attack(self.avatar))

    def test_cannot_attack_into_refuge(self):
        player_pos: Vector = self.avatar.position
        self.bot.position = player_pos + Vector(0, 1)
        locations: dict[Vector, list[GameObject]] = {
            player_pos: [Refuge(player_pos.x, player_pos.y), self.avatar],
            self.bot.position: [self.bot],
        }
        game_board = GameBoard(0, Vector(1, 2), locations)
        game_board.generate_map()
        self.refuge_controller.handle_actions(ActionType.NONE, self.player, game_board)
        self.bot_vision_controller.handle_actions(self.avatar, self.bot, game_board)
        self.assertFalse(self.bot.can_attack(self.avatar))


