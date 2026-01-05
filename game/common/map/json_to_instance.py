from typing import Type
from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.map.wall import Wall
from game.common.stations.occupiable_station import OccupiableStation
from game.common.stations.refuge import Refuge
from game.common.stations.station import Station
from game.fnaacm.bots.crawler_bot import CrawlerBot
from game.fnaacm.bots.dumb_bot import DumbBot
from game.fnaacm.bots.ian_bot import IANBot
from game.fnaacm.bots.jumper_bot import JumperBot
from game.fnaacm.bots.support_bot import SupportBot
from game.fnaacm.map.coin_spawner import CoinSpawner
from game.fnaacm.map.door import Door
from game.fnaacm.map.vent import Vent
from game.fnaacm.stations.battery_spawner import BatterySpawner
from game.fnaacm.stations.generator import Generator
from game.fnaacm.stations.scrap_spawner import ScrapSpawner


OBJECT_TYPE_TO_CLASS: dict[ObjectType, Type] = {
    ObjectType.AVATAR: Avatar,
    ObjectType.BATTERY: BatterySpawner,
    ObjectType.COIN: CoinSpawner,
    ObjectType.DOOR: Door,
    ObjectType.GENERATOR: Generator,
    ObjectType.OCCUPIABLE_STATION: OccupiableStation,
    ObjectType.REFUGE: Refuge,
    ObjectType.SCRAP_SPAWNER: ScrapSpawner,
    ObjectType.STATION: Station,
    ObjectType.VENT: Vent,
    ObjectType.WALL: Wall,
}
_BOT_TYPES: set[Type] = {CrawlerBot, DumbBot, IANBot, JumperBot, SupportBot}
_BOT_CLASS_NAME_TO_CLASS: dict[str, Type]  = dict(zip(map(lambda t: t.__name__, _BOT_TYPES), _BOT_TYPES))

def json_to_instance(data: dict) -> GameObject:
    obj_type = ObjectType(data['object_type'])
    if obj_type == ObjectType.BOT:
        return _BOT_CLASS_NAME_TO_CLASS[data['__class__']]().from_json(data)
    return OBJECT_TYPE_TO_CLASS[obj_type]().from_json(data)
