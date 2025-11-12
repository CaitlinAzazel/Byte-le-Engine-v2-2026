import unittest, pytest

from game.common.map.game_board import GameBoard
from game.config import PATH_TO_LDTK_PROJECT
from game.fnaacm.map.door import Door
from game.utils.ldtk_helpers import ldtk_to_locations
from game.utils.vector import Vector


EXPECTED_MAP_SIZE = Vector(8, 8)


class TestLDtkHelpers(unittest.TestCase):
    def setUp(self) -> None:
        map_size = Vector(8, 8)
        door = Door()
        second_door = Door()
        locations = {

        }
        self.expected_game_board = GameBoard(locations=locations, map_size=map_size)

    def test_loads_ldtk_file(self):
        locations, _ = ldtk_to_locations(PATH_TO_LDTK_PROJECT, level_identifier='test')
        self.assertGreater(len(locations.keys()), 0)

    def test_correct_map_size(self):
        _, map_size = ldtk_to_locations(PATH_TO_LDTK_PROJECT, level_identifier='Test')
        self.assertEqual(map_size, EXPECTED_MAP_SIZE)

    def test_correct_entity_count(self):
        # TODO:
        self.assertTrue(False)

    def test_correct_entity_field_values(self):
        # TODO:
        self.assertTrue(False)
