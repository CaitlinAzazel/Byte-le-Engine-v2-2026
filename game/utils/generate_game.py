import random

from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.map.wall import Wall
from game.fnaacm.map.door import Door
from game.fnaacm.map.vent import Vent
from game.fnaacm.stations.generator import Generator
from game.utils.ldtk_json import LayerInstance, ldtk_json_from_dict
from game.utils.vector import Vector
from game.config import *
from game.utils.helpers import read_json_file, write_json_file
from game.common.map.game_board import GameBoard

def load_entities(game_board: GameBoard, entity_layer: LayerInstance):
    for entity in entity_layer.entity_instances:
        position = Vector(entity.grid[0], entity.grid[1])
        game_object: GameObject | None = None
        match entity.identifier:
            case 'Door':
                game_object = Door()
            case 'Generator':
                game_object = Generator()
                for field in entity.field_instances:
                    match field.identifier:
                        case 'cost':
                            game_object.cost = field.value
        if game_object is None:
            raise ValueError(f'unknown entity identifier: {entity.identifier}')
        placed = game_board.place(position, game_object)
        assert placed, f'failed to place game_object ({entity.identifier}) @ <{position.x},{position.y}>'


def load_collisions(game_board: GameBoard, collision_layer: LayerInstance):
    for i in range(len(collision_layer.int_grid_csv)):
        x = i // game_board.map_size.x
        y = i - x * game_board.map_size.x
        position = Vector(x, y)
        tile_type = collision_layer.int_grid_csv[i]
        match tile_type:
            case LDtkCollisionType.WALL:
                game_board.place(position, Wall())
            case LDtkCollisionType.VENT:
                game_board.place(position, Vent())

def game_board_from_ldtk() -> GameBoard:
    json_data = read_json_file(LDTK_MAP_FILE_PATH)
    ldtk_json = ldtk_json_from_dict(json_data)
    assert len(ldtk_json.levels) == 1, f'this is a dumb hack for the current project; fix if needed'

    level = ldtk_json.levels[0]
    layers = level.layer_instances
    assert layers is not None
    # all layers should (?) have the same grid size 
    assert len(layers) > 0, f'this is another dumb hack for the current project; fix if needed'

    game_board = GameBoard(map_size=Vector(layers[0].c_wid, layers[0].c_hei))
    game_board.generate_map()
    for layer in layers:
        match layer.identifier:
            case 'Entities':
                load_entities(game_board, layer)
            case 'Collision':
                load_collisions(game_board, layer)

    return game_board

def generate(seed: int = random.randint(0, 1000000000)):
    """
    This method is what generates the game_map. This method is slow, so be mindful when using it. A seed can be set as
    the parameter; otherwise, a random one will be generated. Then, the method checks to make sure the location for
    storing logs exists. Lastly, the game map is written to the game file.
    :param seed:
    :return: None
    """

    print(f'Generating game map... seed: {seed}')

    temp: GameBoard = GameBoard(seed, map_size=Vector(6, 6), locations={Vector(1, 1): [Avatar(),],
                                                                        Vector(4, 4): [Avatar(),]}, walled=True)
    temp.generate_map()
    data: dict = {'game_board': temp.to_json()}
    # for x in range(1, MAX_TICKS + 1):
    #     data[x] = 'data'

    # Verify logs location exists
    if not os.path.exists(GAME_MAP_DIR):
        os.mkdir(GAME_MAP_DIR)

    # Write game map to file
    write_json_file(data, GAME_MAP_FILE)
