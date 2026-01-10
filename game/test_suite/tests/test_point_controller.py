
import unittest

from game.common.avatar import Avatar
from game.common.enums import ActionType
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.common.stations.refuge import Refuge
from game.controllers.point_controller import PointController
from game.fnaacm.map.vent import Vent
from game.fnaacm.stations.generator import Generator
from game.utils.vector import Vector


class TestPointController(unittest.TestCase):
    def setUp(self) -> None:
        self.point_controller = PointController()
        self.avatar: Avatar = Avatar()
        self.generator1 = Generator(cost=0, point_bonus=6)
        self.generator2 = Generator(cost=0, point_bonus=7)
        self.game_board: GameBoard = GameBoard(0, map_size=Vector(2, 2), locations={
            Vector(0, 0): [self.avatar],
            Vector(1, 0): [self.generator1],
            Vector(0, 1): [self.generator2],
        })
        self.game_board.generate_map()
        Refuge.reset_global_state()

    def test_points_given_every_turn(self):
        self.assertEqual(self.avatar.score, 0)
        turns = 13
        for _ in range(turns):
            self.point_controller.handle_actions(self.avatar, self.game_board)
        self.assertGreater(self.avatar.score, 0)
        self.assertEqual(self.avatar.score, self.point_controller.base_points_per_turn * turns)

    def test_no_points_while_in_refuge(self):
        Refuge.global_occupied = True
        self.assertEqual(self.avatar.score, 0)
        self.point_controller.handle_actions(self.avatar, self.game_board)
        self.assertEqual(self.avatar.score, 0)

    def test_active_generator_point_bonus(self):
        self.generator1.activate()
        turns = 9
        for _ in range(turns):
            self.point_controller.handle_actions(self.avatar, self.game_board)
        expected_points_per_turn = self.generator1.passive_point_bonus + self.point_controller.base_points_per_turn
        self.assertEqual(self.avatar.score, turns * expected_points_per_turn)

    def test_multiple_active_generators_point_bonus(self):
        self.generator1.activate()
        self.generator2.activate()
        turns = 10
        for _ in range(turns):
            self.point_controller.handle_actions(self.avatar, self.game_board)
        expected_points_per_turn = self.generator1.passive_point_bonus + self.generator2.passive_point_bonus + self.point_controller.base_points_per_turn
        self.assertEqual(self.avatar.score, turns * expected_points_per_turn)

    def test_inactive_generators_no_point_bonus(self):
        turns = 4
        for _ in range(turns):
            self.point_controller.handle_actions(self.avatar, self.game_board)
        expected_points_per_turn = self.point_controller.base_points_per_turn
        self.assertEqual(self.avatar.score, turns * expected_points_per_turn)

    def test_vent_reduces_multiplier(self):
        self.game_board.place(self.avatar.position, Vent())
        expected = self.point_controller.base_multiplier - 0.5
        actual = self.point_controller.calculate_multiplier(self.avatar, self.game_board)
        self.assertEqual(expected, actual)
