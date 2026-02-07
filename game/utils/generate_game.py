import os
import random

from game.common.game_object import GameObject
from game.config import GAME_MAP_DIR, GAME_MAP_FILEPATH, PATH_TO_LDTK_PROJECT, USE_PRECOMPILED_MAP
from game.utils.helpers import write_json_file
from game.common.map.game_board import GameBoard
from game.utils.ldtk_helpers import map_data_from_ldtk_file
from game.utils.vector import Vector


def generate(seed: int = random.randint(0, 1000000000)):
    """
    This method is what generates the game_map. This method is slow, so be mindful when using it. A seed can be set as
    the parameter; otherwise, a random one will be generated. Then, the method checks to make sure the location for
    storing logs exists. Lastly, the game map is written to the game file.
    :param seed:
    :return: None
    """

    print(f'Generating game map... seed: {seed}')
    print(f'Using precompiled map? {USE_PRECOMPILED_MAP}')

    locations: dict[Vector, list[GameObject]]
    map_size: Vector
    if USE_PRECOMPILED_MAP:
        from game.map_data import MAP_DICT, MAP_SIZE
        locations = GameBoard.locations_from_json_dict(MAP_DICT)
        map_size = Vector.new_from_json(MAP_SIZE)
    else:
        locations, map_size = map_data_from_ldtk_file(PATH_TO_LDTK_PROJECT)

    temp: GameBoard = GameBoard(seed, map_size, locations, True)
    temp.generate_map()
    data: dict = {'game_board': temp.to_json()}
    # for x in range(1, MAX_TICKS + 1):
    #     data[x] = 'data'

    # Verify logs location exists
    if not os.path.exists(GAME_MAP_DIR):
        os.mkdir(GAME_MAP_DIR)

    # Write game map to file
    write_json_file(data, GAME_MAP_FILEPATH)
