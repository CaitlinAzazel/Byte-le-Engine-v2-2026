from enum import Enum, auto


class DebugLevel(Enum):
    NONE = auto()
    CLIENT = auto()
    CONTROLLER = auto()
    ENGINE = auto()


class ObjectType(Enum):
    NONE = auto()
    ACTION = auto()
    PLAYER = auto()
    AVATAR = auto()
    GAMEBOARD = auto()
    VECTOR = auto()
    TILE = auto()
    WALL = auto()
    ITEM = auto()
    OCCUPIABLE = auto()
    STATION = auto()
    OCCUPIABLE_STATION = auto()
    STATION_EXAMPLE = auto()
    STATION_RECEIVER_EXAMPLE = auto()
    OCCUPIABLE_STATION_EXAMPLE = auto()
    GAME_OBJECT_CONTAINER = auto()
    GENERATOR = auto()
    SCRAP = auto()
    SCRAP_SPAWNER = auto()
    VENT = auto()
    BATTERY_SPAWNER = auto()
    REFUGE = auto()
    DOOR = auto()
    BOT = auto()
    COIN_SPAWNER = auto()
    CRAWLER_BOT = auto()
    DUMB_BOT = auto()
    IAN_BOT = auto()
    JUMPER_BOT = auto()
    SUPPORT_BOT = auto()

BOT_OBJECT_TYPES = {
    ObjectType.BOT,
    ObjectType.CRAWLER_BOT,
    ObjectType.DUMB_BOT,
    ObjectType.IAN_BOT,
    ObjectType.JUMPER_BOT,
    ObjectType.SUPPORT_BOT,
}

class ActionType(Enum):
    NONE = auto()
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    INTERACT_UP = auto()
    INTERACT_DOWN = auto()
    INTERACT_LEFT = auto()
    INTERACT_RIGHT = auto()
    INTERACT_CENTER = auto()
    SELECT_SLOT_0 = auto()
    SELECT_SLOT_1 = auto()
    SELECT_SLOT_2 = auto()
    SELECT_SLOT_3 = auto()
    SELECT_SLOT_4 = auto()
    SELECT_SLOT_5 = auto()
    SELECT_SLOT_6 = auto()
    SELECT_SLOT_7 = auto()
    SELECT_SLOT_8 = auto()
    SELECT_SLOT_9 = auto()
    PLACE_ITEM_UP = auto()
    PLACE_ITEM_DOWN = auto()
    PLACE_ITEM_LEFT = auto()
    PLACE_ITEM_RIGHT = auto()
    ATTACK_UP = auto()
    ATTACK_DOWN = auto()
    ATTACK_LEFT = auto()
    ATTACK_RIGHT = auto()
    ATTACK_TOP_RIGHT = auto()
    ATTACK_BOTTOM_RIGHT = auto()
    ATTACK_BOTTOM_LEFT = auto()
    ATTACK_TOP_LEFT = auto()
