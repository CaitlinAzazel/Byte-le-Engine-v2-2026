import random

from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.map.wall import Wall
from game.fnaacm.map.door import Door
from game.fnaacm.map.vent import Vent
from game.fnaacm.stations.battery import Battery
from game.fnaacm.stations.generator import Generator
from game.utils.ldtk_json import EntityInstance, LayerInstance, ldtk_json_from_dict
from game.utils.vector import Vector
from game.config import *
from game.utils.helpers import read_json_file, write_json_file
from game.common.map.game_board import GameBoard

ENTITY_LOAD_PRIORITY: dict[str, int] = {
    LDtkConfig.EntityIdentifier.DOOR: -9999, # load doors at least before generators
}

def get_entity_load_priority(entity: EntityInstance) -> int:
    return ENTITY_LOAD_PRIORITY.get(entity.identifier, 0)

def load_entities(game_board: GameBoard, entity_layer: LayerInstance):
    doors: dict[str, Door] = {}
    sorted_entities = sorted(entity_layer.entity_instances, key=get_entity_load_priority)
    for entity in sorted_entities:
        game_object: GameObject | None = None
        match entity.identifier:
            case LDtkConfig.EntityIdentifier.DOOR:
                game_object = Door()
                doors[entity.iid] = game_object
            case LDtkConfig.EntityIdentifier.GENERATOR:
                game_object = Generator.from_ldtk_entity(entity, doors)
            case LDtkConfig.EntityIdentifier.BATTERY:
                game_object = Battery.from_ldtk_entity(entity)
            case _:
                raise ValueError(f'unhandled entity identifier: "{entity.identifier}"')

        position = Vector(entity.grid[0], entity.grid[1])
        placed = game_board.place(position, game_object)
        if not placed:
            raise RuntimeError(f'failed to place game_object ({entity.identifier}) @ <{position.x},{position.y}>')

def vector_from_index(i: int, map_width: int) -> Vector:
    return Vector(i % map_width, i // map_width)

def load_collisions(game_board: GameBoard, collision_layer: LayerInstance):
    for i in range(len(collision_layer.int_grid_csv)):
        position = vector_from_index(i, game_board.map_size.x)
        collision_type = collision_layer.int_grid_csv[i]
        match collision_type:
            case LDtkConfig.CollisionType.NONE:
                pass
            case LDtkConfig.CollisionType.WALL:
                game_board.place(position, Wall())
            case LDtkConfig.CollisionType.VENT:
                game_board.place(position, Vent())
            case _:
                raise ValueError(f'unhandled collision type: {collision_type}')

def game_board_from_ldtk(path_to_ldtk_file: str) -> GameBoard:
    json_data = read_json_file(path_to_ldtk_file)
    ldtk_json = ldtk_json_from_dict(json_data)
    if len(ldtk_json.levels) < 1:
        raise RuntimeError(f'LDtk file "{path_to_ldtk_file}" has no levels')
    level = ldtk_json.levels[0] # hack for current game; we only have one level
    layers = level.layer_instances
    if layers is None:
        raise RuntimeError(f'layers of level "{level.identifier}" could not be found; check if LDtk project setting "Save levels separately" is enabled')
    if len(layers) < 1:
        raise RuntimeError(f'level "{level.identifier}" has no layers')

    game_board = GameBoard()
    # this is why the function doesn't return a locations dict
    # also `load_collisions` currently relies on `GameBoard.map_size`
    game_board.map_size.x = layers[0].c_wid
    game_board.map_size.y = layers[0].c_hei
    game_board.generate_map()
    for layer in layers:
        match layer.identifier:
            case LDtkConfig.LayerIdentifier.ENTITIES:
                load_entities(game_board, layer)
            case LDtkConfig.LayerIdentifier.COLLISIONS:
                load_collisions(game_board, layer)
            case _:
                raise ValueError(f'unhandled layer: {layer.identifier}')

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
