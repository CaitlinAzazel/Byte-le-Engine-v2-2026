import unittest

from game.common.enums import ActionType
from game.common.stations.refuge import Refuge
from game.common.player import Player
from game.common.game_object import GameObject
from game.common.avatar import Avatar
from game.common.map.game_board import GameBoard
from game.common.map.wall import Wall
from game.fnaacm.bots.bot import Bot
from game.controllers.movement_controller import MovementController
from game.controllers.refuge_controller import RefugeController
from game.utils.vector import Vector

class TestRefuge(unittest.TestCase):
    def setUp(self):
        Refuge.reset_global_state()
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
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        for _ in range(10):
            self.assertEqual(self.avatar.position, self.refuge.position)
            self.refuge_controller.handle_actions(ActionType.NONE, self.player, self.game_board)
        self.assertEqual(self.player.avatar.position, Vector(1, 2))

    def test_refuge_ejects_to_east(self):
        Refuge.global_turns_inside = Refuge.MAX_TURNS_INSIDE
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.assertEqual(self.avatar.position, self.refuge.position)
        self.game_board.place(self.refuge.position + Vector( 0, -1), Wall())
        self.game_board.place(self.refuge.position + Vector( 0,  1), Wall())
        self.game_board.place(self.refuge.position + Vector(-1,  0), Wall())
        self.refuge_controller.eject_avatar_from_refuge(self.avatar, self.refuge.position, self.game_board)
        self.assertEqual(self.avatar.position, self.refuge.position + Vector(1, 0))

    def test_refuge_ejects_to_south(self):
        Refuge.global_turns_inside = Refuge.MAX_TURNS_INSIDE
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.assertEqual(self.avatar.position, self.refuge.position)
        self.game_board.place(self.refuge.position + Vector( 0, -1), Wall())
        self.game_board.place(self.refuge.position + Vector( 1,  0), Wall())
        self.game_board.place(self.refuge.position + Vector(-1,  0), Wall())
        self.refuge_controller.eject_avatar_from_refuge(self.avatar, self.refuge.position, self.game_board)
        self.assertEqual(self.avatar.position, self.refuge.position + Vector(0, 1))

    def test_refuge_ejects_to_west(self):
        Refuge.global_turns_inside = Refuge.MAX_TURNS_INSIDE
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.assertEqual(self.avatar.position, self.refuge.position)
        self.game_board.place(self.refuge.position + Vector( 0, -1), Wall())
        self.game_board.place(self.refuge.position + Vector( 0,  1), Wall())
        self.game_board.place(self.refuge.position + Vector( 1,  0), Wall())
        self.refuge_controller.eject_avatar_from_refuge(self.avatar, self.refuge.position, self.game_board)
        self.assertEqual(self.avatar.position, self.refuge.position + Vector(-1, 0))

    def test_refuge_ejection_avoids_bots(self):
        Refuge.global_turns_inside = Refuge.MAX_TURNS_INSIDE
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.assertEqual(self.avatar.position, self.refuge.position)
        self.game_board.place(self.refuge.position + Vector( 0, -1), Bot())
        self.game_board.place(self.refuge.position + Vector( 0,  1), Bot())
        self.game_board.place(self.refuge.position + Vector( 1,  0), Bot())
        self.refuge_controller.eject_avatar_from_refuge(self.avatar, self.refuge.position, self.game_board)
        self.assertEqual(self.avatar.position, self.refuge.position + Vector(-1, 0))
