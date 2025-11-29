import unittest
from game.utils.vector import Vector
from game.common.map.game_board import GameBoard
from game.common.map.wall import Wall
from game.fnaacm.map.vent import Vent
from game.controllers.pathfind_controller import a_star_path

class TestPathfindController(unittest.TestCase):
    def setUp(self):
        self.board = GameBoard(map_size=Vector(5, 5))
        self.board.generate_map()

    def test_simple_path(self):
        start = Vector(0, 0)
        goal = Vector(2, 0)
        path = a_star_path(start, goal, self.board)
        expected = [Vector(0, 0), Vector(1, 0), Vector(2, 0)]
        self.assertEqual([v.as_tuple() for v in path], [v.as_tuple() for v in expected])

    def test_path_blocked_by_wall(self):
        self.board.place(Vector(1, 0), Wall())
        start = Vector(0, 0)
        goal = Vector(2, 0)
        path = a_star_path(start, goal, self.board)
        # Should go around wall
        self.assertNotIn(Vector(1, 0), path)

    def test_path_can_go_through_vent_if_allowed(self):
        self.board.place(Vector(1, 0), Vent())
        start = Vector(0, 0)
        goal = Vector(2, 0)
        path = a_star_path(start, goal, self.board, allow_vents=True)
        self.assertIn(Vector(1, 0), path)

    def test_path_blocks_vent_if_not_allowed(self):
        self.board.place(Vector(1, 0), Vent())
        start = Vector(0, 0)
        goal = Vector(2, 0)
        path = a_star_path(start, goal, self.board, allow_vents=False)
        self.assertNotIn(Vector(1, 0), path)

if __name__ == "__main__":
    unittest.main()
