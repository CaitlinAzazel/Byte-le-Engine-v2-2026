from game.common.enums import ActionType
from game.utils.helpers import flip_dict
from game.utils.vector import Vector


ATTACK_TO_DIRECTION = {
    ActionType.ATTACK_UP: Vector(0, -1, read_only=True),
    ActionType.ATTACK_DOWN: Vector(0, 1, read_only=True),
    ActionType.ATTACK_LEFT: Vector(-1, 0, read_only=True),
    ActionType.ATTACK_RIGHT: Vector(1, 0, read_only=True),
    ActionType.ATTACK_TOP_LEFT: Vector(-1, -1, read_only=True),
    ActionType.ATTACK_BOTTOM_LEFT: Vector(-1, 1, read_only=True),
    ActionType.ATTACK_TOP_RIGHT: Vector(1, -1, read_only=True),
    ActionType.ATTACK_BOTTOM_RIGHT: Vector(1, 1, read_only=True),
}
"""
expects Vectors whose components are clamped between -1 and 1
"""
DIRECTION_TO_ATTACK = flip_dict(ATTACK_TO_DIRECTION)

MOVE_TO_DIRECTION_STR = {
    ActionType.MOVE_UP: 'up',
    ActionType.MOVE_DOWN: 'down',
    ActionType.MOVE_LEFT: 'left',
    ActionType.MOVE_RIGHT: 'right',
}
MOVE_TO_DIRECTION = {
    ActionType.MOVE_UP: Vector(x=0, y=-1, read_only=True),
    ActionType.MOVE_DOWN: Vector(x=0, y=1, read_only=True),
    ActionType.MOVE_LEFT: Vector(x=-1, y=0, read_only=True),
    ActionType.MOVE_RIGHT: Vector(x=1, y=0, read_only=True),
}
"""
expects Vectors whose components are clamped between -1 and 1
"""
DIRECTION_TO_MOVE = flip_dict(MOVE_TO_DIRECTION)

INTERACT_TO_DIRECTION = {
    ActionType.INTERACT_UP: Vector(x=0, y=-1, read_only=True),
    ActionType.INTERACT_DOWN: Vector(x=0, y=1, read_only=True),
    ActionType.INTERACT_LEFT: Vector(x=-1, y=0, read_only=True),
    ActionType.INTERACT_RIGHT: Vector(x=1, y=0, read_only=True),
    ActionType.INTERACT_CENTER: Vector(0, 0, read_only=True),
}
"""
expects Vectors whose components are clamped between -1 and 1
"""
DIRECTION_TO_INTERACT = flip_dict(INTERACT_TO_DIRECTION)
