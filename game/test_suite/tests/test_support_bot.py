import unittest

from game.common.avatar import Avatar
from game.common.enums import ActionType
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.attack_controller import Attack_Controller
from game.fnaacm.bots.bot import Bot
from game.fnaacm.bots.support_bot import SupportBot
from game.utils.vector import Vector

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.supportBot = SupportBot()
        self.attack_controller = Attack_Controller()
        self.attacking_bot = Bot()
        self.player_avatar = Avatar(position=Vector(0, 0))
        self.target_player = Player(avatar=self.player_avatar)

    def build_board(self, objects: dict[Vector, list[GameObject]]):
        gb = GameBoard(0, Vector(4, 4), objects)
        gb.generate_map()
        return gb

    def hit_player(self):
        self.attacking_bot.position = Vector(0, 1)
        board = self.build_board({
            Vector(0, 0): [self.player_avatar],
            Vector(0, 1): [self.attacking_bot],
            Vector(1, 0): [],
            Vector(1, 1): [],
        })

        self.attack_controller.handle_actions(
            ActionType.ATTACK_UP,
            self.target_player,
            board,
            self.attacking_bot
        )

    def test_init(self):
        self.assertEqual(self.supportBot.turnedOn, True)
        self.assertEqual(self.supportBot.is_stunned, False)
        self.assertEqual(self.supportBot.stun_counter, 0)

    def test_turnedOn_method_returns_correct_value(self):
        self.assertFalse(self.supportBot.turned_on())
        self.supportBot.turnedOn = True
        self.assertTrue(self.supportBot.turned_on())

    def test_flip_state(self):
        self.supportBot.turnedOn = False
        self.supportBot.flip_state()
        self.assertTrue(self.supportBot.turnedOn)

    def test_player_hit_stun(self):
        self.hit_player()
        self.assertEqual(self.supportBot.stun_counter, 0)

    def test_double_player_stun(self):
        self.hit_player()
        self.assertEqual(self.supportBot.stun_counter, 0)
        self.hit_player()
        self.assertEqual(self.supportBot.stun_counter, 0)

    # def test_scrap_stun(self):
    #     self.supportBot.scrap_stun()
    #     self.assertTrue(self.supportBot.is_stunned)
    #     self.assertEqual(self.supportBot.stun_counter, 25)
    #     self.assertFalse(self.supportBot.turnedOn)
    #
    # def test_double_scrap_stun(self):
    #     self.supportBot.scrap_stun()
    #     self.assertTrue(self.supportBot.is_stunned)
    #     self.assertEqual(self.supportBot.stun_counter, 25)
    #     self.assertFalse(self.supportBot.turnedOn)
    #     self.supportBot.scrap_stun()
    #     self.assertTrue(self.supportBot.is_stunned)
    #     self.assertEqual(self.supportBot.stun_counter, 25)
    #     self.assertFalse(self.supportBot.turnedOn)
    #
    # def test_player_stun_then_scrap_stun(self):
    #     self.hit_player()
    #     self.supportBot.scrap_stun()
    #     self.assertTrue(self.supportBot.is_stunned)
    #     self.assertEqual(self.supportBot.stun_counter, 25)
    #     self.assertFalse(self.supportBot.turnedOn)
    #
    # def test_scrap_stun_then_player_stun(self):
    #     self.supportBot.scrap_stun()
    #     self.hit_player()
    #     self.assertTrue(self.supportBot.is_stunned)
    #     self.assertEqual(self.supportBot.stun_counter, 30)
    #     self.assertFalse(self.supportBot.turnedOn)

    def test_action_not_stunned(self):
        self.assertEqual(self.supportBot.is_stunned, False)
        self.supportBot.stunned()
        self.assertEqual(self.supportBot.is_stunned, False)
        self.assertEqual(self.supportBot.stun_counter, 1)

    def test_action_stunned(self):
        self.supportBot.stun = True
        self.supportBot.stun_counter = 1
        self.supportBot.stunned()
        self.assertEqual(self.supportBot.stun_counter, 2)

    def test_action_un_stun(self):
        self.supportBot.is_stunned = True
        self.supportBot.stun_counter = 4
        self.supportBot.stunned()
        self.assertEqual(self.supportBot.is_stunned, False)
        self.assertEqual(self.supportBot.stun_counter, 0)