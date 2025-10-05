import unittest

from game.common.enums import ObjectType
from game.common.avatar import Avatar
from game.common.items.item import Item
from game.common.map.game_object_container import GameObjectContainer
from game.common.stations.station import Station
from game.common.stations.occupiable_station import OccupiableStation
from game.common.map.wall import Wall
from game.controllers.movement_controller import MovementController
from game.utils.vector import Vector
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.test_suite.utils import spell_check


class TestGameBoard(unittest.TestCase):
    """
    `Test Gameboard Notes:`

        This class tests the different methods in the Gameboard class. This file is worthwhile to look at to understand
        the GamebBoard class better if there is still confusion on it.

        *This class tests the Gameboard specifically when the map is generated.*
    """

    def setUp(self) -> None:
        self.item: Item = Item(10, None)
        self.wall: Wall = Wall()
        self.avatar: Avatar = Avatar()
        self.locations: dict[Vector, list[GameObject]] = {
            Vector(0, 0): [Station(None),],
            Vector(1, 0): [OccupiableStation(self.item), Station(None),],
            Vector(2, 0): [OccupiableStation(self.item), OccupiableStation(self.item), OccupiableStation(self.item),
                           OccupiableStation(self.item)],
            Vector(0, 1): [self.avatar,],
            Vector(1, 1): [self.wall,],
        }

        self.game_board: GameBoard = GameBoard(1, Vector(3, 3), self.locations, False)
        self.game_board.generate_map()

    # test that seed cannot be set after generate_map
    def test_seed_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.seed = 20
        self.assertTrue(spell_check(str(e.exception), 'GameBoard variables cannot be changed once '
                                                      'generate_map is run.', False))

    # test that map_size cannot be set after generate_map
    def test_map_size_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.map_size = Vector(1, 1)
        self.assertTrue(spell_check(str(e.exception), 'GameBoard variables cannot be changed once '
                                                      'generate_map is run.', False))

    # test that locations cannot be set after generate_map
    def test_locations_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.locations = self.locations
        self.assertTrue(spell_check(str(e.exception), 'GameBoard variables cannot be changed once '
                                                      'generate_map is run.', False))

    # test that locations raises RuntimeError even with incorrect data type
    def test_locations_incorrect_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.locations = Vector(1, 1)
        self.assertTrue(spell_check(str(e.exception), 'GameBoard variables cannot be changed once '
                                                      'generate_map is run.', False))

    # test that walled cannot be set after generate_map
    def test_walled_fail(self):
        with self.assertRaises(RuntimeError) as e:
            self.game_board.walled = False
        self.assertTrue(spell_check(str(e.exception), 'GameBoard variables cannot be changed once '
                                                      'generate_map is run.', False))

    # test that get_objects works correctly with stations
    def test_get_objects_station(self):
        stations: list[tuple[Vector, list[GameObject]]] = self.game_board.get_objects(ObjectType.STATION)
        self.assertTrue(all(map(lambda station: isinstance(station[1][0], Station), stations)))
        self.assertEqual(len(stations), 2)

    # test that get_objects works correctly with occupiable stations
    def test_get_objects_occupiable_station(self):
        occupiable_stations: list[tuple[Vector, list[GameObject]]] = self.game_board.get_objects(
            ObjectType.OCCUPIABLE_STATION)
        self.assertTrue(
            all(map(lambda occupiable_station: isinstance(occupiable_station[1][0], OccupiableStation),
                    occupiable_stations)))
        objects_stacked = [x[1] for x in occupiable_stations]
        objects_unstacked = [x for xs in objects_stacked for x in xs]
        self.assertEqual(len(objects_unstacked), 5)

    def test_get_objects_occupiable_station_2(self):
        occupiable_stations: list[tuple[Vector, list[GameObject]]] = self.game_board.get_objects(
            ObjectType.OCCUPIABLE_STATION)

        # checks if the list of GameObjects has 4 OccupiableStations in that list
        self.assertTrue(any(map(lambda vec_list: len(vec_list[1]) == 4, occupiable_stations)))

        objects_stacked = [x[1] for x in occupiable_stations]
        objects_unstacked = [x for xs in objects_stacked for x in xs]
        self.assertEqual(len(objects_unstacked), 5)

    # test that get_objects works correctly with avatar
    def test_get_objects_avatar(self):
        avatars: list[tuple[Vector, list[GameObject]]] = self.game_board.get_objects(ObjectType.AVATAR)
        self.assertTrue(all(map(lambda avatar: isinstance(avatar[1][0], Avatar), avatars)))
        self.assertEqual(len(avatars), 1)

    # test that get_objects works correctly with walls
    def test_get_objects_wall(self):
        walls: list[tuple[Vector, list[GameObject]]] = self.game_board.get_objects(ObjectType.WALL)
        self.assertTrue(all(map(lambda wall: isinstance(wall[1][0], Wall), walls)))
        self.assertEqual(len(walls), 1)

    # testing a successful case of the place_on_top_of method
    def test_place_on_top_of_occupiable(self):
        success: bool = self.game_board.place(Vector(2, 0), Avatar())
        container: GameObjectContainer = self.game_board.game_map[Vector(2, 0)]

        # test return value is true
        self.assertTrue(success)

        # test all occupiable stations are still in the list
        [self.assertEqual(container.get_objects()[x].object_type, ObjectType.OCCUPIABLE_STATION)
         for x in range(len(container.get_objects()) - 1)]

        # test that the avatar is at the top of the list
        self.assertEqual(container.get_objects()[-1].object_type, ObjectType.AVATAR)

    # testing another successful case of the place_on_top method
    def test_place_under_top_object(self):
        success: bool = self.game_board.place(Vector(0, 0), OccupiableStation())
        container: GameObjectContainer = self.game_board.game_map[Vector(0, 0)]

        # test return value is true
        self.assertTrue(success)

        # test that the UnoccupiableStation is first before the Station
        self.assertEqual(container.get_objects()[0].object_type, ObjectType.OCCUPIABLE_STATION)
        self.assertEqual(container.get_objects()[1].object_type, ObjectType.STATION)
        self.assertEqual(container.get_top().object_type, ObjectType.STATION)

    # testing an invalid coordinate
    def test_place_on_top_of_invalid_coordinate(self):
        before: GameObjectContainer = self.game_board.game_map[Vector(0, 0)]
        result: bool = self.game_board.place(Vector(100, 0), Avatar())

        self.assertFalse(result)

        # test that the list hasn't changed
        self.assertEqual(before, self.game_board.game_map[Vector(0, 0)])

    # testing placing a None value raises an error
    def test_place_on_top_of_not_game_object(self):
        before: GameObjectContainer = self.game_board.game_map[Vector(0, 0)]
        result: bool = self.game_board.place(Vector(100, 0), Avatar())

        self.assertFalse(result)

        # test that the list hasn't changed
        self.assertEqual(before, self.game_board.game_map[Vector(0, 0)])

    # testing placing an unoccupiable object on another unoccupiable object fails
    def test_place_on_top_of_unoccupiable(self):
        before: GameObjectContainer = self.game_board.game_map[Vector(0, 0)]

        # test placing a GameObject that doesn't inherit from occupiable works
        result: bool =self.game_board.place(Vector(0, 0), Station())
        self.assertFalse(result)

        # test that the list hasn't changed
        self.assertEqual(before, self.game_board.game_map[Vector(0, 0)])

        # test placing a non-GameObject doesn't work.
        result: bool = self.game_board.place(Vector(0, 0), MovementController())
        self.assertFalse(result)

        # test that the list hasn't changed
        self.assertEqual(before, self.game_board.game_map[Vector(0, 0)])

    # testing placing on top/beneath a wall raises an error
    def test_place_on_top_of_wall(self):
        pass

    def test_get_objects_from(self):
        result: list[GameObject] = self.game_board.get_objects_from(Vector(2, 0), ObjectType.OCCUPIABLE_STATION)

        # check if the resulting lists are the same
        self.assertEqual(result, self.game_board.game_map[Vector(2, 0)].get_objects())

    def test_get_objects_from_fail(self):
        result = self.game_board.get_objects_from(Vector(50, 0), ObjectType.OCCUPIABLE_STATION)
        self.assertEqual(result, [])

    def test_object_is_found_at(self):
        result: bool = self.game_board.object_is_found_at(Vector(0, 0), ObjectType.STATION)
        self.assertTrue(result)

    def test_object_is_found_at_fail(self):
        result: bool = self.game_board.object_is_found_at(Vector(0, 0), ObjectType.OCCUPIABLE_STATION)
        self.assertFalse(result)

    # test that the removed object is returned
    def test_remove_object_from(self):
        before: GameObject = self.game_board.get_objects_from(Vector(0, 0), ObjectType.STATION)[0]
        after: GameObject = self.game_board.remove(Vector(0, 0), ObjectType.STATION)
        self.assertEqual(before, after)

    # test that the returned value is None due to the object not being found
    def test_remove_object_from_none(self):
        result = self.game_board.remove(Vector(0, 0), ObjectType.OCCUPIABLE_STATION)
        self.assertEqual(result, None)

    # test that None is returned because of a bad coordinate
    def test_remove_object_from_bad_coord(self):
        result = self.game_board.remove(Vector(100, 0), ObjectType.STATION)
        self.assertEqual(result, None)

    # test that all matching objects in the entire map are returned
    def test_get_objects(self):
        result: list[tuple[Vector, list[GameObject]]] = self.game_board.get_objects(ObjectType.OCCUPIABLE_STATION)
        [[self.assertEqual(x.object_type, ObjectType.OCCUPIABLE_STATION) for x in sublist[1]] for sublist in result]

    # test that an ObjectType that's not on the map returns an empty list
    def test_get_objects_fail(self):
        result: list[tuple[Vector, list[GameObject]]] = self.game_board.get_objects(ObjectType.OCCUPIABLE)
        self.assertEqual(result, [])

    # ensure the avatar position is stored properly
    def test_avatar_pos_check(self):
        pos: Vector = self.avatar.position
        self.assertEqual(pos, Vector(0, 1))

    def test_overlapped_pos_calculator(self):
        actual_positions = GameBoard.get_positions_overlapped_by_line(Vector(0, 0), Vector(1, 2))
        expected_positions = [
            Vector(0, 0),
            Vector(0, 1),
            Vector(1, 1),
            Vector(1, 2)
        ]
        for position in actual_positions:
            self.assertIn(position, expected_positions, f'did not find {position} in expected')
            print(f'{position.x} {position.y}')
        for position in expected_positions:
            self.assertIn(position, actual_positions, f'did not find {position} in actual')

    # TODO: test edge cases like
    # WP
    # BW
    # W = wall
    # P = player
    # B = bot

    # test json method
    def test_game_board_json(self):
        data: dict = self.game_board.to_json()
        temp: GameBoard = GameBoard().from_json(data)

        self.assertEqual(self.game_board.seed, temp.seed)
        self.assertEqual(self.game_board.map_size, temp.map_size)
        self.assertEqual(self.game_board.walled, temp.walled)
        self.assertEqual(self.game_board.event_active, temp.event_active)

        self.assertEqual(self.game_board.game_map.keys(), temp.game_map.keys())
        self.assertTrue(self.game_board.game_map.values(), temp.game_map.values())
