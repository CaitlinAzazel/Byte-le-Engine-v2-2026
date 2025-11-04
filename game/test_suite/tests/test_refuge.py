import unittest

from game.common.enums import ActionType
from game.common.stations.refuge import Refuge
from game.common.player import Player
from game.common.game_object import GameObject
from game.common.avatar import Avatar
from game.common.map.game_board import GameBoard
from game.controllers.movement_controller import MovementController
from game.controllers.refuge_controller import RefugeController
from game.utils.vector import Vector

class TestRefuge(unittest.TestCase):
    def setUp(self):
        self.refuge = Refuge(1,1)
        self.avatar_start_pos = self.refuge.position.add_x(-1)
        self.avatar = Avatar(position=self.avatar_start_pos)
        self.locations: dict[Vector, list[GameObject]] = {
            self.refuge.position: [self.refuge],
            self.avatar_start_pos: [self.avatar],
        }
        self.game_board = GameBoard(0, Vector(4,4), self.locations)
        self.player = Player(avatar=self.avatar)
        self.refuge_controller = RefugeController()
        self.movement_controller = MovementController()
        self.game_board.generate_map()

    def test_refuge_occupiable(self):
        # passes when ran individually
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.assertEqual(self.avatar.position, self.refuge.position)
        self.refuge_controller.handle_actions(ActionType.NONE, self.player, self.game_board)
        self.assertTrue(Refuge.global_occupied)

    def test_refuge_nonoccupiable(self):
        Refuge.global_turns_outside = 0
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.refuge_controller.handle_actions(ActionType.NONE, self.player, self.game_board)
        self.assertEqual(self.avatar.position, self.avatar_start_pos)
        self.assertFalse(Refuge.global_occupied)

    def test_refuge_ejection(self):
        # passes when ran individually
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        for _ in range(10):
            self.assertEqual(self.avatar.position, self.refuge.position)
            self.refuge_controller.handle_actions(ActionType.NONE, self.player, self.game_board)
        self.assertEqual(self.player.avatar.position, Vector(1, 2))

    # TODO: test cases for ejecting to E, S, W,

    # TODO: check if ejection avoids bots

    # TODO: waiting on point system
    def test_refuge_point_blockade(self):
        ...
