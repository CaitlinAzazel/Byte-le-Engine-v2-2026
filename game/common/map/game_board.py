import ast
import random
import json
from math import floor
from typing import Self, Type

from game.common.enums import *
from game.common.game_object import GameObject
from game.common.map.game_object_container import GameObjectContainer
from game.common.map.wall import Wall
from game.common.map.occupiable import Occupiable
from game.fnaacm.map.coin_spawner import CoinSpawner, CoinSpawnerList
from game.fnaacm.map.scrap_spawner_list import ScrapSpawnerList
from game.fnaacm.stations.battery_spawner import BatterySpawner
from game.fnaacm.stations.generator import Generator
from game.fnaacm.map.battery_spawner_list import BatterySpawnerList
from game.fnaacm.stations.scrap_spawner import ScrapSpawner
from game.utils.vector import Vector
from game.common.map.json_to_instance import json_to_instance


class GameBoard(GameObject):
    """
    `GameBoard Class Notes:`

    Map Size:
    ---------
        map_size is a Vector object, allowing you to specify the size of the (x, y) plane of the game board.
        For example, a Vector object with an 'x' of 5 and a 'y' of 7 will create a board 5 tiles wide and
        7 tiles long.

        Example:
        ::
            _ _ _ _ _  y = 0
            |       |
            |       |
            |       |
            |       |
            |       |
            |       |
            _ _ _ _ _  y = 6

    -----

    Locations:
    ----------
        This is the bulkiest part of the generation.

        The locations field is a dictionary with a key of a tuple of Vectors, and the value being a list of
        GameObjects (the key **must** be a tuple instead of a list because Python requires dictionary keys to be
        immutable).

        This is used to assign the given GameObjects the given coordinates via the Vectors. This is done in two ways:

        Statically:
            If you want a GameObject to be at a specific coordinate, ensure that the key-value pair is
            *ONE* Vector and *ONE* GameObject.
            An example of this would be the following:
            ::
                locations = { (vector_2_4) : [station_0] }

            In this example, vector_2_4 contains the coordinates (2, 4). (Note that this naming convention
            isn't necessary, but was used to help with the concept). Furthermore, station_0 is the
            GameObject that will be at coordinates (2, 4).

        Dynamically:
            If you want to assign multiple GameObjects to different coordinates, use a key-value
            pair of any length.

            **NOTE**: The length of the tuple and list *MUST* be equal, otherwise it will not
            work. In this case, the assignments will be random. An example of this would be the following:
            ::
                locations =
                {
                    (vector_0_0, vector_1_1, vector_2_2) : [station_0, station_1, station_2]
                }

            (Note that the tuple and list both have a length of 3).

            When this is passed in, the three different vectors containing coordinates (0, 0), (1, 1), or
            (2, 2) will be randomly assigned station_0, station_1, or station_2.

            If station_0 is randomly assigned at (1, 1), station_1 could be at (2, 2), then station_2 will be at (0, 0).
            This is just one case of what could happen.

        Lastly, another example will be shown to explain that you can combine both static and
        dynamic assignments in the same dictionary:
        ::
            locations =
                {
                    (vector_0_0) : [station_0],
                    (vector_0_1) : [station_1],
                    (vector_1_1, vector_1_2, vector_1_3) : [station_2, station_3, station_4]
                }

        In this example, station_0 will be at vector_0_0 without interference. The same applies to
        station_1 and vector_0_1. However, for vector_1_1, vector_1_2, and vector_1_3, they will randomly
        be assigned station_2, station_3, and station_4.

    -----

    Walled:
    -------
        This is simply a bool value that will create a wall barrier on the boundary of the game_board. If
        walled is True, the wall will be created for you.

        For example, let the dimensions of the map be (5, 7). There will be wall Objects horizontally across
        x = 0 and x = 4. There will also be wall Objects vertically at y = 0 and y = 6

        Below is a visual example of this, with 'x' being where the wall Objects are.

        Example:
        ::
            x x x x x   y = 0
            x       x
            x       x
            x       x
            x       x
            x       x
            x x x x x   y = 6
    """

    @staticmethod
    def insert_location(locations: dict[Vector, list[GameObject]], position: Vector, game_object: GameObject):
        if position in locations:
            locations[position].append(game_object)
        else:
            locations[position] = [game_object]

    def __init__(self, seed: int | None = None, map_size: Vector = Vector(),
                 locations: dict[Vector, list[GameObject]] = {}, walled: bool = False):

        super().__init__()
        # game_map is initially going to be None. Since generation is slow, call generate_map() as needed
        self.game_map: dict[Vector, GameObjectContainer] | None = None
        self.seed: int | None = seed
        random.seed(seed)
        self.object_type: ObjectType = ObjectType.GAMEBOARD
        self.event_active: int | None = None
        self.map_size: Vector = map_size
        # when passing Vectors as a tuple, end the tuple of Vectors with a comma, so it is recognized as a tuple
        self.locations: dict = locations
        self.walled: bool = walled
        self.generators: dict[Vector, Generator] = {}
        self.battery_spawners: BatterySpawnerList = BatterySpawnerList()
        self.scrap_spawners: ScrapSpawnerList = ScrapSpawnerList()
        self.coin_spawners: CoinSpawnerList = CoinSpawnerList()

    @property
    def seed(self) -> int:
        return self.__seed

    @seed.setter
    def seed(self, seed: int | None) -> None:
        if self.game_map is not None:
            raise RuntimeError(f'{self.__class__.__name__} variables cannot be changed once generate_map is run.')
        if seed is not None and not isinstance(seed, int):
            raise ValueError(
                f'{self.__class__.__name__}.seed must be an int. '
                f'It is a(n) {seed.__class__.__name__} with the value of {seed}.')
        self.__seed = seed

    @property
    def game_map(self) -> dict[Vector, GameObjectContainer] | None:
        return self.__game_map

    @game_map.setter
    def game_map(self, game_map: dict[Vector, GameObjectContainer] | None) -> None:
        if game_map is not None and not isinstance(game_map, dict) \
                and any([not isinstance(vec, Vector) or not isinstance(go_container, GameObjectContainer)
                         for vec, go_container in game_map.items()]):
            raise ValueError(
                f'{self.__class__.__name__}.game_map must be a dict[Vector, GameObjectContainer].'
                f'It has a value of {game_map}.'
            )

        self.__game_map = game_map

    @property
    def map_size(self) -> Vector:
        return self.__map_size

    @map_size.setter
    def map_size(self, map_size: Vector) -> None:
        if self.game_map is not None:
            raise RuntimeError(f'{self.__class__.__name__} variables cannot be changed once generate_map is run.')
        if map_size is None or not isinstance(map_size, Vector):
            raise ValueError(
                f'{self.__class__.__name__}.map_size must be a Vector. '
                f'It is a(n) {map_size.__class__.__name__} with the value of {map_size}.')
        self.__map_size = map_size

    @property
    def locations(self) -> dict:
        return self.__locations

    @locations.setter
    def locations(self, locations: dict[Vector, list[GameObject]]) -> None:
        if self.game_map is not None:
            raise RuntimeError(f'{self.__class__.__name__} variables cannot be changed once generate_map is run.')
        if locations is not None and not isinstance(locations, dict):
            raise ValueError(
                f'Locations must be a dict. The key must be a tuple of Vector Objects, '
                f'and the value a list of GameObject. '
                f'It is a(n) {locations.__class__.__name__} with the value of {locations}.')

        self.__locations = locations

    @property
    def walled(self) -> bool:
        return self.__walled

    @walled.setter
    def walled(self, walled: bool) -> None:
        if self.game_map is not None:
            raise RuntimeError(f'{self.__class__.__name__} variables cannot be changed once generate_map is run.')
        if walled is None or not isinstance(walled, bool):
            raise ValueError(
                f'{self.__class__.__name__}.walled must be a bool. '
                f'It is a(n) {walled.__class__.__name__} with the value of {walled}.')

        self.__walled = walled

    def generate_map(self) -> None:
        # Dictionary Init
        self.game_map = self.__map_init()

    def __map_init(self) -> dict[Vector, GameObjectContainer]:
        output: dict[Vector, GameObjectContainer] = dict()

        # Update all Avatar positions if they are to be placed on the map
        for vec, objs in self.locations.items():
            for obj in objs:
                if hasattr(obj, 'position'):
                    obj.position = vec

                # assume that none of the following will be added after __map_init
                if isinstance(obj, Generator):
                    self.generators[vec] = obj
                elif isinstance(obj, BatterySpawner):
                    self.battery_spawners.append(obj)
                elif isinstance(obj, ScrapSpawner):
                    self.scrap_spawners.append(obj)
                elif isinstance(obj, CoinSpawner):
                    self.coin_spawners.append(obj)

        if self.walled:
            # Generate the walls
            output.update({Vector(x=x, y=0): GameObjectContainer([Wall(), ]) for x in range(self.map_size.x)})
            output.update({Vector(x=x, y=self.map_size.y - 1): GameObjectContainer([Wall(), ])
                           for x in range(self.map_size.x)})
            output.update({Vector(x=0, y=y): GameObjectContainer([Wall(), ]) for y in range(1, self.map_size.y - 1)})
            output.update({Vector(x=self.map_size.x - 1, y=y): GameObjectContainer([Wall(), ])
                           for y in range(1, self.map_size.y - 1)})

        # convert locations dict to go_container
        output.update({vec: GameObjectContainer(objs) for vec, objs in self.locations.items()})

        return output

    def get(self, coords: Vector) -> GameObjectContainer | None:
        """
        A GameObjectContainer object returned given the coordinates. If the coordinates are valid but are not in the
        game_map yet, a new GameObjectContainer is created and is stored in a new entry in the game_map dictionary.

        :param coords:
        :return: GameObjectContainer or None
        """
        if self.is_valid_coords(coords) and self.game_map.get(coords, None) is None:
            self.game_map[coords] = GameObjectContainer()

        return self.game_map.get(coords)

    def place(self, coords: Vector, game_obj: GameObject | None) -> bool:
        """
        Places the given object at the given coordinates if they are valid. A boolean is returned to represent a
        successful placement
        :param coords:
        :param game_obj:
        :return: True or False for a successful placement of the given object
        """
        if not self.is_valid_coords(coords):
            return False
        if not self.get(coords).place(game_obj):
            return False
        if hasattr(game_obj, 'position'):
            game_obj.position = coords
        return True

    def get_objects_from(self, coords: Vector, object_type: ObjectType | None = None) -> list[GameObject]:
        """
        Returns a list of GameObjects from the given, valid coordinates. If an ObjectType is specified, only that
        ObjectType will be returned. If an ObjectType is not specified, the entire list of GameObjects will be
        returned. If nothing is found, an empty list is given.
        :param coords:
        :param object_type:
        :return: a list of GameObjects
        """
        return self.game_map[coords].get_objects(object_type) if coords in self.game_map else []

    def remove(self, coords: Vector, object_type: ObjectType) -> GameObject | None:
        """
        Removes the first instance of the given object type from the coordinates if they are valid. Returns None if
        invalid coordinates are given.
        :param coords:
        :param object_type:
        :return: GameObject or None
        """
        to_return: GameObject | None = self.game_map[coords].remove(object_type) if coords in self.game_map else None

        # if there is a None value paired with the coordinate key after removal, delete that entry from the dict
        if self.is_valid_coords(coords) and self.get(coords).get_top() is None:
            self.game_map.pop(coords, None)

        return to_return

    def get_top(self, coords: Vector) -> GameObject | None:
        """
        Returns the last object in the GameObjectContainer (i.e, the top-most object in the stack).
        Returns None if invalid coordinates are given or there are no objects at that position.
        :param coords:
        :return: GameObject or None
        """
        if not self.is_valid_coords(coords):
            return None
        return self.get(coords).get_top()

    def object_is_found_at(self, coords: Vector, object_type: ObjectType) -> bool:
        """
        Searches for an object with the given object type at the given coordinate. If no object is found, or if the
        coordinate is invalid, return False.
        :param coords:
        :param object_type:
        :return: True or False to determine if the object is at that location
        """

        if not self.is_valid_coords(coords):
            return False

        result: list[GameObject] | None = self.game_map[coords].get_objects(object_type)
        return result is not None and len(result) > 0

    def is_valid_coords(self, coords: Vector) -> bool:
        """
        Check if the given coordinates are valid. In order to do so, the following criteria must be met:
            - The given coordinates must be in the self.game_map dictionary keys first
            - Otherwise, the coordinates must be within the size of the game map

        :param coords:
        :return: True if the coordinates are already in the map or are within the map size
        """

        return (0 <= coords.x < self.map_size.x) and (0 <= coords.y < self.map_size.y)

    def is_occupiable(self, coords: Vector) -> bool:
        return self.is_valid_coords(coords) and (self.get(coords).get_top() is None or
                                                 isinstance(self.get(coords).get_top(), Occupiable))

    def can_object_occupy(self, coords: Vector, game_object: GameObject) -> bool:
        """
        returns whether `game_object` can occupy the space at `coords`
        """
        if not self.is_occupiable(coords):
            return False

        occupiable = self.get_top(coords)
        if occupiable is None:
            return True

        if not isinstance(occupiable, Occupiable):
            return False
        return occupiable.can_be_occupied_by(game_object)

    # Returns the Vector and a list of GameObject for whatever objects you are trying to get
    # TODO: CHANGE RETURN TYPE TO BE A DICT NOT A LIST OF TUPLES
    def get_objects(self, look_for: ObjectType) -> list[tuple[Vector, list[GameObject]]]:
        """
        Zips together the game map's keys and values. A nested for loop then iterates through the zipped lists, and
        looks for any objects that have the same object type that was passed in. A list of tuples containing the
        coordinates and the objects found is returned. If the given object type isn't found on the map, then an empty
        list is returned
        """

        results: list[tuple[Vector, list[GameObject]]] = []

        # Loops through the zipped list
        # DICTIONARY COMPREHENSION HERE PLEASE
        for vec, go_container in self.game_map.items():
            found: list[GameObject] = go_container.get_objects(look_for)  # add the matching object to the found list

            # add values to result if something was found
            if len(found) > 0:
                results.append((vec, found))  # Add tuple pairings and objects found

        return results


    def update_object_position(self, position: Vector, game_object: GameObject) -> None:
        assert hasattr(game_object, 'position')

        # remove the avatar from its previous location
        self.remove(game_object.position, game_object.object_type)

        # add the avatar to the top of the list of the coordinate
        self.place(position, game_object)

        # reassign the avatar's position
        game_object.position = position

    def to_json(self) -> dict:
        data: dict[str, object] = super().to_json()
        temp: dict[Vector, GameObjectContainer] | None = {str(vec.to_json()): go_container.to_json() for
                                                          vec, go_container in
                                                          self.game_map.items()} if self.game_map is not None else None
        data['game_map'] = temp
        data["seed"] = self.seed
        data["map_size"] = self.map_size.to_json()
        data["location_vectors"] = [vec.to_json() for vec in self.locations.keys()] if self.locations is not None \
            else None
        data["location_objects"] = [[obj.to_json() for obj in v] for v in
                                    self.locations.values()] if self.locations is not None else None
        data["walled"] = self.walled
        data['event_active'] = self.event_active

        data['generators'] = {str(pos.to_json()): generator.to_json() for (pos, generator) in self.generators.items()}
        data['battery_spawners'] = self.battery_spawners.to_json()
        data['scrap_spawners'] = self.scrap_spawners.to_json()
        data['coin_spawners'] = self.coin_spawners.to_json()
        # FIXME: the data in the above are accurate but the ones in game_map are not
        # which prevents the visualizer from working properly

        return data

    def generate_event(self, start: int, end: int) -> None:
        self.event_active = random.randint(start, end)

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.seed: int | None = data["seed"]
        self.map_size: Vector = Vector().from_json(data["map_size"])

        self.locations: dict[Vector, list[GameObject]] = {
            Vector().from_json(k): [json_to_instance(obj) for obj in v] for k, v in
            zip(data["location_vectors"], data["location_objects"])} if data["location_vectors"] is not None else None

        self.walled: bool = data["walled"]
        self.event_active: int = data['event_active']

        # json.ast.literal_eval is `abstract syntax tree`
        # the vector objects were stored as a dictionary in a string format
        # json.ast.literal_eval takes in the string, converts it to a dict, and uses that for the from_json()

        self.game_map: dict[Vector, GameObjectContainer] = {
            Vector().from_json(ast.literal_eval(k)): GameObjectContainer().from_json(v)
            for k, v in data['game_map'].items()} if data['game_map'] is not None else None

        self.generators = {
            Vector().from_json(json.loads(pos_json_str.replace('\'', '\"'))):
            Generator().from_json(gen_json) 
            for pos_json_str, gen_json in data['generators'].items()}
        self.battery_spawners = BatterySpawnerList().from_json(data['battery_spawners'])
        self.scrap_spawners = ScrapSpawnerList().from_json(data['scrap_spawners'])
        self.coin_spawners = CoinSpawnerList().from_json(data['coin_spawners'])

        return self
