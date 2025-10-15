import unittest

from game.common.enums import ActionType
from game.common.stations.refuge import Refuge
from game.common.player import Player
from game.common.game_object import GameObject
from game.common.avatar import Avatar
from game.common.map.game_board import GameBoard
from game.controllers.movement_controller import MovementController
from game.utils.vector import Vector

class TestRefuge(unittest.TestCase):
    def setUp(self):

        self.refuge = Refuge(1,1)
        self.avatar = Avatar()
        self.locations: dict[Vector, list[GameObject]] = {
            Vector(1, 1): [self.refuge],
            Vector(0, 1): [self.avatar]
        }
        self.game_board = GameBoard(None, Vector(4,4), self.locations, True)
        self.actions: list[ActionType] = []
        self.player = Player(None, None, self.actions, self.avatar)
        self.controller = MovementController()
        self.game_board.generate_map()

    def test_refuge_occupiable(self):
        self.controller.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.assertTrue(self.player.avatar.position == Vector(1,1) )
        Refuge.refuge_tick(self.avatar)
        self.assertTrue(Refuge.global_occupied)

    def test_refuge_nonoccupiable(self):
        Refuge.global_turns_outside = 0
        self.controller.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        Refuge.refuge_tick(self.avatar)
        self.assertTrue(self.player.avatar.position == Vector(0,1) )
        self.assertFalse(Refuge.global_occupied)

    def test_refuge_ejection(self):
        self.controller.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        for i in range (10):
            print(Refuge.global_turns_inside)
            Refuge.refuge_tick(self.avatar, self.game_board)
            print(self.player.avatar.position)
            print(Refuge.global_turns_inside)
        self.assertTrue(self.player.avatar.position == Vector(1, 2) )

    # TODO: test cases for ejecting to E, S, W,

    # TODO: check if ejection avoids bots

    # TODO: waiting on point system
    def test_refuge_point_blockade(self):
        ...