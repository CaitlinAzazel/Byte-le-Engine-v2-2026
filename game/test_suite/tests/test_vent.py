import unittest

from game.common.avatar import Avatar
from game.common.enums import ActionType
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.movement_controller import MovementController
from game.fnaacm.map.vent import Vent
from game.utils.vector import Vector


class TestVent(unittest.TestCase):
    def setUp(self) -> None:
        self.vent: Vent = Vent()
        self.vent_pos: Vector = Vector(1, 1)

        self.avatar = Avatar()
        self.avatar.position=self.vent_pos+Vector(-1, 0)

        # TODO: add animatronics to corresponding lists
        self.eligible: list[GameObject] = [self.avatar, ]
        self.ineligible: list[GameObject] = [GameObject(), ]

        self.locations: dict[Vector, list[GameObject]] | None = {
            self.vent_pos: [self.vent, ],
        }
        self.game_board = GameBoard(0, Vector(4, 4), self.locations, True)  # create 4x4 gameboard
        self.game_board.generate_map()
        self.movement_controller = MovementController()
        self.player = Player(avatar=self.avatar)

    def test_avatar_can_occupy(self):
        [self.assertTrue(self.vent.can_occupy(game_object)) for game_object in self.eligible]

    def test_others_cannot_occupy(self):
        [self.assertFalse(self.vent.can_occupy(game_object)) for game_object in self.ineligible]

    def test_avatar_can_move_into(self):
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.assertEqual(self.avatar.position, self.vent_pos)

    # TODO:
    def test_crawler_can_move_into(self):
        pass

    # TODO: 
    def test_others_cannot_move_into(self):
        pass
