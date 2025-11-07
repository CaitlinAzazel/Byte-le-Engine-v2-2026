import unittest
from unittest.mock import MagicMock
from game.fnaacm.bots.ian_bot import IANBot
from game.common.enums import ActionType
from game.utils.vector import Vector


class DummyAvatar:
    def __init__(self, x, y):
        self.position = Vector(x, y)
        self.object_type = "AVATAR"


class DummyPlayer:
    def __init__(self, x, y):
        self.avatar = DummyAvatar(x, y)


class DummyWorld:
    def __init__(self, width=5, height=5):
        self.width = width
        self.height = height
        self.grid = {}

    def is_valid_coords(self, vec):
        return 0 <= vec.x < self.width and 0 <= vec.y < self.height

    def get_top(self, vec):
        return self.grid.get((vec.x, vec.y), None)

    def remove(self, vec, obj_type):
        self.grid.pop((vec.x, vec.y), None)

    def place(self, vec, obj):
        self.grid[(vec.x, vec.y)] = obj


class TestIANBot(unittest.TestCase):
    def setUp(self):
        self.world = DummyWorld()
        self.player = DummyPlayer(4, 4)
        self.bot = IANBot("Test Ian")
        self.bot.avatar = DummyAvatar(0, 0)
        self.bot.attack_controller = MagicMock()

    def test_moves_every_two_turns(self):
        """IAN moves every 2nd turn."""
        self.bot.take_turn(1, self.player, self.world)
        self.assertEqual(self.bot.avatar.position, Vector(0, 0))

        self.bot.take_turn(2, self.player, self.world)
        self.assertIn(self.bot.avatar.position, [Vector(1, 0), Vector(0, 1)])

    def test_attacks_cardinal_only(self):
        """IAN attacks only cardinal directions."""
        self.bot.avatar = DummyAvatar(2, 2)
        self.player.avatar.position = Vector(2, 3)

        called = {"action": None}

        def fake_handle(action, player_obj, world_obj, bot_obj):
            called["action"] = action

        self.bot.attack_controller.handle_actions = fake_handle

        self.bot.take_turn(2, self.player, self.world)
        self.assertEqual(called["action"], ActionType.ATTACK_DOWN)

        # Diagonal should not attack
        called["action"] = None
        self.player.avatar.position = Vector(3, 3)
        self.bot.take_turn(2, self.player, self.world)
        self.assertIsNone(called["action"])


if __name__ == "__main__":
    unittest.main()
