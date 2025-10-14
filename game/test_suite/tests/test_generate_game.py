import unittest

from game.config import LDTK_MAP_FILE_PATH
from game.utils.generate_game import ldtk_to_locations


class TestGenerateGame(unittest.TestCase):
    def test_loads_ldtk_file(self):
        locations, map_size = ldtk_to_locations(LDTK_MAP_FILE_PATH)
        self.assertGreater(len(locations.keys()), 0)
