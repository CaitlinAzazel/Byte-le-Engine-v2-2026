from typing import Self
from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.map.wall import Wall
from game.config import LDtk
from game.fnaacm.bots.crawler_bot import CrawlBot
from game.fnaacm.bots.dumb_bot import DumbBot
from game.fnaacm.bots.ian_bot import IANBot
from game.fnaacm.bots.jumper_bot import JumpBot
from game.fnaacm.bots.support_bot import SupportBot
from game.fnaacm.map.coin_spawner import CoinSpawner
from game.fnaacm.map.door import Door
from game.fnaacm.map.vent import Vent
from game.fnaacm.stations.battery_spawner import BatterySpawner
from game.fnaacm.stations.generator import Generator
from game.fnaacm.stations.scrap_spawner import ScrapSpawner
from game.common.stations.refuge import Refuge
from game.utils.helpers import read_json_file
from game.utils.ldtk_json import EntityInstance, LayerInstance, Level, ldtk_json_from_dict 
from game.utils.vector import Vector


"""
unspecified entities have a default priority of 0
highest = first; lowest = last
"""
ENTITY_LOAD_PRIORITY: dict[str, int] = {
    LDtk.EntityIdentifier.DOOR: -9999, # load doors at least before generators
}

def get_entity_load_priority(entity: EntityInstance) -> int:
    return ENTITY_LOAD_PRIORITY.get(entity.identifier.lower(), 0)

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
                spawned_entity = IANBot()
            case LDtk.SpawnedEntityType.CRAWLER:
                spawned_entity = CrawlBot()
            case LDtk.SpawnedEntityType.JUMPER:
                spawned_entity = JumpBot()
            case LDtk.SpawnedEntityType.SUPPORT:
                spawned_entity = SupportBot()
            case LDtk.SpawnedEntityType.DUMMY:
                spawned_entity = DumbBot()
            case _:
                raise ValueError(f'unhandled spawner entity type: "{field.value}"')
    if spawned_entity is None:
        raise RuntimeError(f'could not determine spawner\'s entity type; best guess is "{parsed_value}"')
    return spawned_entity


def load_entities(locations: dict[Vector, list[GameObject]], entity_layer: LayerInstance):
    doors: dict[str, Door] = {}
    sorted_entities = sorted(entity_layer.entity_instances, key=get_entity_load_priority)
    for entity in sorted_entities:
        game_object: GameObject
        match entity.identifier.lower():
            case LDtk.EntityIdentifier.DOOR:
                game_object = Door()
                doors[entity.iid] = game_object
            case LDtk.EntityIdentifier.GENERATOR:
                game_object = Generator.from_ldtk_entity(entity, doors)
            case LDtk.EntityIdentifier.BATTERY:
                game_object = BatterySpawner.from_ldtk_entity(entity)
            case LDtk.EntityIdentifier.ENTITY_SPAWN:
                game_object = get_spawned_entity_from_spawner(entity)
            case LDtk.EntityIdentifier.SCRAP:
                game_object = ScrapSpawner.from_ldtk_entity(entity)
            case LDtk.EntityIdentifier.COIN:
                game_object = CoinSpawner.from_ldtk_entity(entity)
            case _:
                raise ValueError(f'unhandled entity identifier: "{entity.identifier}"')

        position = Vector(entity.grid[0], entity.grid[1])
        GameBoard.insert_location(locations, position, game_object)

def load_collisions(locations: dict[Vector, list[GameObject]], collision_layer: LayerInstance, map_width: int):
    for i in range(len(collision_layer.int_grid_csv)):
        position = Vector(i % map_width, i // map_width)
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
                game_object = Refuge(position.x, position.y)
            case _:
                raise ValueError(f'unhandled collision type: {collision_type}')

        if game_object is None:
            continue
        GameBoard.insert_location(locations, position, game_object)

def ldtk_to_locations(path_to_ldtk_file: str, level_identifier: str = 'production') -> tuple[dict[Vector, list[GameObject]], Vector]:
    """
    :param level_identifier: case-insensitive identifier of the level to parse
    :return: a tuple containing a Locations dict as used in GameBoard and the size of the map
    """
    json_data = read_json_file(path_to_ldtk_file)
    ldtk_json = ldtk_json_from_dict(json_data)
    assert len(ldtk_json.levels) >= 1, f'LDtk file "{path_to_ldtk_file}" has no levels'
    level: Level | None = None
    for l in ldtk_json.levels:
        if l.identifier.lower() == level_identifier.lower():
            level = l
            break
    assert not (level is None), f'LDtk file ({path_to_ldtk_file}) does not contain a level with identifier "{level_identifier}"'

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
