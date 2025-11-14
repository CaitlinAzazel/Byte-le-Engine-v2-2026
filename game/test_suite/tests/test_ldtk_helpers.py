import unittest

from game.common.map.game_board import GameBoard
from game.common.map.wall import Wall
from game.config import PATH_TO_LDTK_PROJECT
from game.fnaacm.map.door import Door
from game.fnaacm.map.vent import Vent
from game.fnaacm.stations.scrap_spawner import ScrapSpawner
from game.fnaacm.stations.battery_spawner import BatterySpawner
from game.fnaacm.map.coin_spawner import CoinSpawner
from game.fnaacm.stations.generator import Generator
from game.common.stations.refuge import Refuge
from game.utils.ldtk_helpers import ldtk_to_locations
from game.utils.vector import Vector


EXPECTED_MAP_SIZE = Vector(8, 8)
EXPECTED_TOTAL_INSTANCES = 15
TYPES_WITHOUT_DATA = {Wall, Vent}

class TestLDtkHelpers(unittest.TestCase):
    def setUp(self) -> None:
        map_size = Vector(8, 8)
        door = Door()
        second_door = Door()
        locations = {
            Vector(0, 0): [Wall()],
            Vector(0, 1): [Vent()],
            Vector(0, 2): [Refuge(0, 2)],
            Vector(1, 0): [Generator(cost=99, point_bonus=2025, doors=[door, second_door])],
            Vector(1, 1): [door],
            Vector(1, 2): [BatterySpawner(cooldown_duration=99, recharge_amount=2025)],
            Vector(1, 3): [ScrapSpawner(respawn_rate=99)],
            Vector(1, 4): [CoinSpawner(cooldown_duration=99, points=67)],
            Vector(7, 7): [second_door]
        }
        self.expected_game_board = GameBoard(locations=locations, map_size=map_size)
        self.expected_game_board.generate_map()

    def test_loads_ldtk_file(self):
        locations, _ = ldtk_to_locations(PATH_TO_LDTK_PROJECT, level_identifier='test')
        self.assertGreater(len(locations.keys()), 0)

    def test_correct_map_size(self):
        _, map_size = ldtk_to_locations(PATH_TO_LDTK_PROJECT, level_identifier='Test')
        self.assertEqual(map_size, EXPECTED_MAP_SIZE)

    def test_correct_entity_count(self):
        locations, _ = ldtk_to_locations(PATH_TO_LDTK_PROJECT, level_identifier='test')
        self.assertEqual(sum(map(len, locations.values())), EXPECTED_TOTAL_INSTANCES)

    def test_correct_entity_field_values(self):
        locations, map_size = ldtk_to_locations(PATH_TO_LDTK_PROJECT, level_identifier='test')
        game_board = GameBoard(0, map_size, locations)
        game_board.generate_map()
        for position in self.expected_game_board.game_map.keys():
            expected = self.expected_game_board.get_top(position)
            actual = game_board.get_top(position)
            self.assertEqual(type(expected), type(actual))
            # don't check if the objects are equal unless they actually store data
            if any(map(lambda t: isinstance(actual, t), TYPES_WITHOUT_DATA)):
                continue
            self.assertEqual(expected, actual)
