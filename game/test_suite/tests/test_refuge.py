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
        self.refuge.refuge_tick(self.avatar)

    def test_refuge_nonoccupiable(self):
        self.refuge.ejection_reset = 0
        self.controller.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.assertTrue(self.player.avatar.position == Vector(0,1) )

    def test_refuge_ejection(self):
        self.controller.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        for i in range (11):
            self.refuge.refuge_countdown(self.avatar)
            print(self.player.avatar.position)
            print(self.refuge.countdown_timer)
        self.assertTrue(self.player.avatar.position == Vector(1, 2) )

   # def test_refuge_point_blockade(self):