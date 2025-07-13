from enum import Enum, auto

"""
**NOTE:** The use of the enum structure is to make is easier to execute certain tasks. It also helps with
identifying types of Objects throughout the project.

When developing the game, add any extra enums as necessary.
"""


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
    VENT = auto()
    BATTERY = auto()


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
    """
    These last 10 enums are for selecting a slot from the Avatar class' inventory.
    You can add/remove these as needed for the purposes of your game. 
    """
