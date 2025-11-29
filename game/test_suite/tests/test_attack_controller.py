import unittest
from game.controllers.attack_controller import Attack_Controller
from game.common.enums import ActionType
from game.common.avatar import Avatar
from game.common.player import Player
from game.common.map.game_board import GameBoard
from game.common.game_object import GameObject
from game.fnaacm.bots.bot import Bot
from game.fnaacm.map.vent import Vent
from game.common.stations.station import Station
from game.utils.vector import Vector


class TestAttackController(unittest.TestCase):
    def setUp(self):
        self.attack_controller = Attack_Controller()
        self.attacking_bot = Bot()
        self.player_avatar = Avatar(position=Vector(0, 0))
        self.target_player = Player(avatar=self.player_avatar)

    def build_board(self, objects: dict[Vector, list[GameObject]]):
        gb = GameBoard(0, Vector(4, 4), objects)
        gb.generate_map()
        return gb

    def test_attack_hits_player_up(self):
        self.attacking_bot.position = Vector(0, 1)

        board = self.build_board({
            Vector(0, 0): [self.player_avatar],
            Vector(0, 1): [self.attacking_bot]
        })

        self.attack_controller.handle_actions(
            ActionType.ATTACK_UP,
            self.target_player,
            board,
            self.attacking_bot
        )

        self.assertTrue(self.attacking_bot.has_attacked)

    def test_attack_does_not_hit_bot(self):
        other_bot = Bot()
        self.attacking_bot.position = Vector(0, 1)

        board = self.build_board({
            Vector(0, 0): [other_bot],
            Vector(0, 1): [self.attacking_bot]
        })

        self.attack_controller.handle_actions(
            ActionType.ATTACK_UP,
            Player(avatar=Avatar(Vector(1, 1))),  # attacking player's controller avatar doesn't matter
            board,
            self.attacking_bot
        )

        self.assertFalse(self.attacking_bot.has_attacked)

    def test_attack_does_not_hit_station(self):
        station = Station(position=Vector(0, 0))
        self.attacking_bot.position = Vector(0, 1)

        board = self.build_board({
            Vector(0, 0): [station],
            Vector(0, 1): [self.attacking_bot]
        })

        self.attack_controller.handle_actions(
            ActionType.ATTACK_UP,
            Player(avatar=Avatar(Vector(1, 1))),
            board,
            self.attacking_bot
        )

        self.assertFalse(self.attacking_bot.has_attacked)

    def test_attack_blocked_by_vent(self):
        self.attacking_bot.position = Vector(0, 1)

        board = self.build_board({
            Vector(0, 0): [Vent(), self.player_avatar],
            Vector(0, 1): [self.attacking_bot]
        })

        self.attack_controller.handle_actions(
            ActionType.ATTACK_UP,
            self.target_player,
            board,
            self.attacking_bot
        )

        self.assertFalse(self.attacking_bot.has_attacked)
    def test_attack_turns_generators_off_when_avatar_hit(self):
        # Setup bot position
        self.attacking_bot.position = Vector(0, 1)

        # Create generators and set them ON
        class DummyGen:
            def __init__(self):
                self.active = True

        gen1 = DummyGen()
        gen2 = DummyGen()

        board = self.build_board({
            Vector(0, 0): [self.player_avatar],
            Vector(0, 1): [self.attacking_bot]
        })

        # Inject generators into the board
        board.generators = {"g1": gen1, "g2": gen2}

        # Execute attack
        self.attack_controller.handle_actions(
            ActionType.ATTACK_UP,
            self.target_player,
            board,
            self.attacking_bot
        )

        self.assertTrue(self.attacking_bot.has_attacked)
        self.assertFalse(gen1.active)
        self.assertFalse(gen2.active)
    def test_generators_unchanged_when_no_avatar_hit(self):
        # Setup bot position
        self.attacking_bot.position = Vector(0, 1)

        # Generators initially ON
        class DummyGen:
            def __init__(self):
                self.active = True

        gen1 = DummyGen()
        gen2 = DummyGen()

        # Put only a Station (no Avatar) in target tile
        station = GameObject()
        board = self.build_board({
            Vector(0, 0): [station],
            Vector(0, 1): [self.attacking_bot]
        })

        board.generators = {"g1": gen1, "g2": gen2}

        # Execute attack (won't hit Avatar)
        self.attack_controller.handle_actions(
            ActionType.ATTACK_UP,
            Player(avatar=Avatar(Vector(3, 3))),
            board,
            self.attacking_bot
        )

        # Should not attack and should NOT toggle generators
        self.assertFalse(self.attacking_bot.has_attacked)
        self.assertTrue(gen1.active)
        self.assertTrue(gen2.active)
