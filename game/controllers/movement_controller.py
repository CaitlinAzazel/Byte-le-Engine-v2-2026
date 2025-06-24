from game.common.avatar import Avatar
from game.common.player import Player
from game.common.map.game_board import GameBoard
from game.common.enums import *
from game.utils.vector import Vector
from game.controllers.controller import Controller


class MovementController(Controller):
    """
    `Movement Controller Notes:`

        The Movement Controller manages the movement actions the player tries to execute. Players can move up, down,
        left, and right. If the player tries to move into a space that's impassable, they don't move.

        For example, if the player attempts to move into an Occupiable Station (something the player can be on) that is
        occupied by a Wall object (something the player can't be on), the player doesn't move; that is, if the player
        tries to move into anything that can't be occupied by something, they won't move.
    """

    def __init__(self):
        super().__init__()

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard):
        avatar = client.avatar

        direction: Vector
        match action:
            case ActionType.MOVE_UP:
                direction = Vector(x=0, y=-1)
            case ActionType.MOVE_DOWN:
                direction = Vector(x=0, y=1)
            case ActionType.MOVE_LEFT:
                direction = Vector(x=-1, y=0)
            case ActionType.MOVE_RIGHT:
                direction = Vector(x=1, y=0)
            case _:  # default case
                return

        destination: Vector = avatar.position + direction

        # if the top of the given coordinates are not occupiable or are invalid, return to do nothing
        if not world.is_occupiable(destination):
            return

        # remove the avatar from its previous location
        world.remove(avatar.position, ObjectType.AVATAR)

        # add the avatar to the top of the list of the coordinate
        world.place(destination, avatar)

        # reassign the avatar's position
        avatar.position = destination
