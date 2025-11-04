
import unittest

from game.common.avatar import Avatar
from game.common.enums import ActionType
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.common.stations.refuge import Refuge
from game.controllers.point_controller import PointController


class TestPointController(unittest.TestCase):
    def setUp(self) -> None:
        self.point_controller = PointController()
        self.avatar: Avatar = Avatar()
        self.player: Player = Player(avatar=self.avatar)
        self.game_board: GameBoard = GameBoard(0)
        Refuge.reset_global_state()

    def test_points_given_every_turn(self):
        self.assertEqual(self.avatar.points, 0)
        turns = 13
        for _ in range(turns):
            self.point_controller.handle_actions(ActionType.NONE, self.player, self.game_board)
        self.assertEqual(self.avatar.points, self.point_controller.points_per_turn * turns)

    def test_no_points_while_in_refuge(self):
        Refuge.global_occupied = True
        self.assertEqual(self.avatar.points, 0)
        self.point_controller.handle_actions(ActionType.NONE, self.player, self.game_board)
        self.assertEqual(self.avatar.points, 0)
