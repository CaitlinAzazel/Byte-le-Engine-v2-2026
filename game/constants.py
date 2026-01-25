from game.common.enums import ActionType
from game.utils.helpers import flip_dict
from game.utils.vector import Vector


ATTACK_TO_DIRECTION = {
    ActionType.ATTACK_UP: Vector(0, -1),
    ActionType.ATTACK_DOWN: Vector(0, 1),
    ActionType.ATTACK_LEFT: Vector(-1, 0),
    ActionType.ATTACK_RIGHT: Vector(1, 0),
    ActionType.ATTACK_TOP_LEFT: Vector(-1, -1),
    ActionType.ATTACK_BOTTOM_LEFT: Vector(-1, 1),
    ActionType.ATTACK_TOP_RIGHT: Vector(1, -1),
    ActionType.ATTACK_BOTTOM_RIGHT: Vector(1, 1),
}
DIRECTION_TO_ATTACK = flip_dict(ATTACK_TO_DIRECTION)

MOVE_TO_DIRECTION = {
    ActionType.MOVE_UP: Vector(x=0, y=-1),
    ActionType.MOVE_DOWN: Vector(x=0, y=1),
    ActionType.MOVE_LEFT: Vector(x=-1, y=0),
    ActionType.MOVE_RIGHT: Vector(x=1, y=0),
}
DIRECTION_TO_MOVE = flip_dict(MOVE_TO_DIRECTION)

INTERACT_TO_DIRECTION = {
    ActionType.INTERACT_UP: Vector(x=0, y=-1),
    ActionType.INTERACT_DOWN: Vector(x=0, y=1),
    ActionType.INTERACT_LEFT: Vector(x=-1, y=0),
    ActionType.INTERACT_RIGHT: Vector(x=1, y=0),
    ActionType.INTERACT_CENTER: Vector(0, 0),
}
DIRECTION_TO_INTERACT = flip_dict(INTERACT_TO_DIRECTION)
