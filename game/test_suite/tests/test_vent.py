import unittest 

from game.common.avatar import Avatar
from game.common.enums import ActionType
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.bot_movement_controller import BotMovementController
from game.controllers.movement_controller import MovementController
from game.fnaacm.bots.crawler_bot import CrawlerBot
from game.fnaacm.bots.dumb_bot import DumbBot
from game.fnaacm.bots.ian_bot import IANBot
from game.fnaacm.bots.jumper_bot import JumpBot
from game.fnaacm.bots.support_bot import SupportBot
from game.fnaacm.map.vent import Vent
from game.utils.vector import Vector


class TestVent(unittest.TestCase):
    def setUp(self) -> None:
        self.movement_controller = MovementController()
        self.bot_movement_controller = BotMovementController()

        self.vent: Vent = Vent()
        self.vent_pos: Vector = Vector(1, 1)

        self.avatar = Avatar()
        self.avatar.position=self.vent_pos+Vector(-1, 0)

        self.crawler = CrawlerBot()
        self.dummy = DumbBot()
        self.ian = IANBot()
        self.jumper = JumpBot()
        self.support = SupportBot()

        # support cannot move so we Do Not care
        self.ineligible_bots = [self.dummy, self.ian, self.jumper, ] 

        self.eligible: list[GameObject] = [self.avatar, self.crawler]
        self.ineligible: list[GameObject] = [GameObject(), self.dummy, self.ian, self.jumper, self.support]

        self.locations: dict[Vector, list[GameObject]] | None = {
            self.vent_pos: [self.vent, ],
        }
        self.game_board = GameBoard(0, Vector(4, 4), self.locations, True)  # create 4x4 gameboard
        self.game_board.generate_map()
        self.player = Player(avatar=self.avatar)

    def test_avatar_can_occupy(self):
        for game_object in self.eligible:
            self.assertTrue(self.vent.can_be_occupied_by(game_object))

    def test_others_cannot_occupy(self):
        for game_object in self.ineligible:
            self.assertFalse(self.vent.can_be_occupied_by(game_object), f'{game_object} should not be able to occupy vents')

    def test_avatar_can_move_into(self):
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.assertEqual(self.avatar.position, self.vent_pos)

    def test_crawler_can_move_into(self):
        self.game_board.place(Vector(1,0) + self.vent_pos, self.crawler)
        self.bot_movement_controller.handle_actions(ActionType.MOVE_LEFT, self.crawler, self.game_board)
        self.assertEqual(self.crawler.position, self.vent_pos, f'{self.crawler.position} != {self.vent_pos}')

    def test_others_cannot_move_into(self):
        for bot in self.ineligible_bots:
            self.setUp()
            initial_pos = self.vent_pos + Vector(1, 0)
            self.game_board.place(initial_pos, bot)
            self.bot_movement_controller.handle_actions(ActionType.MOVE_LEFT, bot, self.game_board)
            self.assertNotEqual(bot.position, self.vent_pos, f'{bot.__class__.__name__} moved into the vent')

