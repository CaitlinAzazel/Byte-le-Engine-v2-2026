import unittest

from game.utils.generate_game import game_board_from_ldtk


class TestGenerateGame(unittest.TestCase):
    def test_loads_ldtk_file(self):
        # TODO: make this test something
        self.assertIsNotNone(game_board_from_ldtk())
