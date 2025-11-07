import unittest
from unittest.mock import MagicMock
from game.fnaacm.bots.crawler_bot import CrawlBot
from game.fnaacm.map.vent import Vent
from game.common.enums import ActionType, ObjectType
from game.utils.vector import Vector


class DummyAvatar:
    def __init__(self, x, y):
        self.position = Vector(x, y)
        self.object_type = ObjectType.AVATAR


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


class TestCrawlerBot(unittest.TestCase):
    def setUp(self):
        self.world = DummyWorld()
        self.player = DummyPlayer(4, 4)
        self.bot = CrawlBot("Test Crawler")
        self.bot.avatar = DummyAvatar(0, 0)
        self.bot.attack_controller = MagicMock()

    def test_moves_every_four_turns(self):
        """Crawler moves only on every 4th turn."""
        for t in range(1, 4):
            self.bot.take_turn(t, self.player, self.world)
            self.assertEqual(self.bot.avatar.position, Vector(0, 0))

        self.bot.take_turn(4, self.player, self.world)
        self.assertIn(self.bot.avatar.position, [Vector(1, 0), Vector(0, 1)])

    def test_attacks_cardinal_only(self):
        """Crawler attacks only cardinal directions."""
        self.bot.avatar = DummyAvatar(3, 2)
        self.player.avatar.position = Vector(3, 3)

        called = {"action": None}

        def fake_handle(action, player_obj, world_obj, bot_obj):
            called["action"] = action

        self.bot.attack_controller.handle_actions = fake_handle

        self.bot.take_turn(4, self.player, self.world)
        self.assertEqual(called["action"], ActionType.ATTACK_DOWN)

        # Diagonal adjacency should not attack
        called["action"] = None
        self.player.avatar.position = Vector(4, 3)
        self.bot.take_turn(4, self.player, self.world)
        self.assertIsNone(called["action"])

    def test_moves_through_vent(self):
        """Crawler pathfinds through vent tiles."""
        vent = Vent()
        self.world.place(Vector(1, 0), vent)

        self.bot.take_turn(4, self.player, self.world)
        self.assertEqual(self.bot.avatar.position, Vector(1, 0))


if __name__ == "__main__":
    unittest.main()
