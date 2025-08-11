import random

from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.map.occupiable import Occupiable
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

"""
unspecified entities have a default priority of 0
highest = first; lowest = last
"""
ENTITY_LOAD_PRIORITY: dict[str, int] = {
    LDtk.EntityIdentifier.DOOR: -9999, # load doors at least before generators
}

def get_entity_load_priority(entity: EntityInstance) -> int:
    return ENTITY_LOAD_PRIORITY.get(entity.identifier, 0)

def get_spawned_entity_from_spawner(spawner: EntityInstance) -> GameObject:
    spawned_entity: GameObject | None = None
    parsed_value: str = ''
    for field in spawner.field_instances:
        if field.identifier.lower() != 'spawned_entity':
            continue

        parsed_value = field.value
        match field.value.lower():
            case LDtk.SpawnedEntityType.PLAYER:
                spawned_entity = Avatar()
            case LDtk.SpawnedEntityType.IAN:
                # TODO:
                spawned_entity = Avatar()
            case LDtk.SpawnedEntityType.CRAWLER:
                # TODO:
                spawned_entity = Avatar()
            case LDtk.SpawnedEntityType.JUMPER:
                # TODO:
                spawned_entity = Avatar()
            case LDtk.SpawnedEntityType.SUPPORT:
                # TODO:
                spawned_entity = Avatar()
            case LDtk.SpawnedEntityType.DUMMY:
                # TODO:
                spawned_entity = Avatar()
            case _:
                raise ValueError(f'unhandled spawner entity type: "{field.value}"')
    if spawned_entity is None:
        raise RuntimeError(f'could not determine spawner\'s entity type; best guess is "{parsed_value}"')
    return spawned_entity


def load_entities(locations: dict[Vector, list[GameObject]], entity_layer: LayerInstance):
    doors: dict[str, Door] = {}
    sorted_entities = sorted(entity_layer.entity_instances, key=get_entity_load_priority)
    for entity in sorted_entities:
        game_object: GameObject | None = None
        match entity.identifier.lower():
            case LDtk.EntityIdentifier.DOOR:
                game_object = Door()
                doors[entity.iid] = game_object
            case LDtk.EntityIdentifier.GENERATOR:
                game_object = Generator.from_ldtk_entity(entity, doors)
            case LDtk.EntityIdentifier.BATTERY:
                game_object = Battery.from_ldtk_entity(entity)
            case LDtk.EntityIdentifier.SPAWN:
                game_object = get_spawned_entity_from_spawner(entity)
            case LDtk.EntityIdentifier.SCRAP:
                # TODO: write a luh scrap spawner and use it here
                ...
            case _:
                raise ValueError(f'unhandled entity identifier: "{entity.identifier}"')
        if game_object is None:
            continue

        position = Vector(entity.grid[0], entity.grid[1])
        GameBoard.insert_location(locations, position, game_object)

def load_collisions(locations: dict[Vector, list[GameObject]], collision_layer: LayerInstance, map_width: int):
    for i in range(len(collision_layer.int_grid_csv)):
        game_object: GameObject | None = None 
        collision_type = collision_layer.int_grid_csv[i]
        match collision_type:
            case LDtk.CollisionType.NONE:
                pass
            case LDtk.CollisionType.WALL:
                game_object = Wall()
            case LDtk.CollisionType.VENT:
                game_object = Vent()
            case LDtk.CollisionType.SAFE_POINT:
                # TODO: replace with hidey hole/refuge/safe point instance
                game_object = Occupiable()
            case _:
                raise ValueError(f'unhandled collision type: {collision_type}')
        if game_object is None:
            continue
        position = Vector(i % map_width, i // map_width)
        GameBoard.insert_location(locations, position, game_object)

def ldtk_to_locations(path_to_ldtk_file: str) -> tuple[dict[Vector, list[GameObject]], Vector]:
    """
    returned vector is the size of the map
    """
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

    map_size = Vector(layers[0].c_wid, layers[0].c_hei)
    locations: dict[Vector, list[GameObject]] = {}
    for layer in layers:
        match layer.identifier.lower():
            case LDtk.LayerIdentifier.ENTITIES:
                load_entities(locations, layer)
            case LDtk.LayerIdentifier.COLLISIONS:
                load_collisions(locations, layer, map_size.x)
            case 'AutoLayer':
                pass
            case _:
                raise ValueError(f'unhandled layer: {layer.identifier}')

    return locations, map_size

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
