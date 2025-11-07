import unittest

from game.config import LDTK_MAP_FILE_PATH
from game.utils.ldtk_helpers import ldtk_to_locations
from game.utils.vector import Vector


class TestLDtkHelpers(unittest.TestCase):
    def test_loads_ldtk_file(self):
        locations, _ = ldtk_to_locations(LDTK_MAP_FILE_PATH)
        self.assertGreater(len(locations.keys()), 0)

    def test_map_size_is_correct(self):
        EXPECTED_MAP_SIZE = Vector(8, 8)
        _, map_size = ldtk_to_locations(LDTK_MAP_FILE_PATH)
        self.assertEqual(map_size, EXPECTED_MAP_SIZE)


