import unittest
from game.common.stations.refuge import Refuge
from game.common.player import Player
from game.common.game_object import GameObject
from game.common.avatar import Avatar
from game.common.map.game_board import GameBoard
from game.controllers.movement_controller import MovementController
from game.utils.vector import Vector

class TestRefuge(unittest.TestCase)
    def setUp(self):
        self.refuge = Refuge(1, 1)
        self.refuge_pos = Vector(1,1)

        self.avatar = Avatar()
        self.avatar.position = Vector(0, 1)
