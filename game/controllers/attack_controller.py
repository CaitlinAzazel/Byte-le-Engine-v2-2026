from game.common.enums import *
from game.controllers.controller import Controller
from game.common.player import Player
from game.common.stations.station import Station
from game.common.map.game_board import GameBoard
from game.utils.vector import Vector

class Attack_Controller(Controller):
    """
    `Attack Controller Notes:`

        The Attack Controller manages the actions the bots try to execute. As the game is played, a bot can
        attack a surrounding player, adjacent stations from where they are currently positioned. For the jumping bot
        they are able to attack the diagonal stations from where they are currently positioned and when boosted both
        the diagonal stations and the adjacent stations from where they are currently positioned.

        Example:
        ::  Normal Bots    Jumper Boost   Jumper Norm
            x x x x x x    x x x x x x    x x x x x x
            x         x    x         x    x         x
            x   O     x    x  O O O  x    x O   P   x
            x O B P   x    x  0 B P  x    x   B     x
            x   O     x    x  O O O  x    x O   O   x
            x x x x x x    x x x x x x    x x x x x x

        The given visual shows what bots can interact with. "B represents the bot; "P" represents the player; "O"\
        represents the spaces that can be interacted with (including where the "P" and "B" is); and
        "x" represents the walls and map border.

        These interactions are managed by using the provided ActionType enums in the enums.py file.
    """

def __init__(self):
    super().__init__()

def handle_actions(self, action: ActionType, client: Player, world: GameBoard, bot: Bot) -> None:
    """
        Given the ActionType for interacting in a direction, the Player's avatar will engage with the object.
        :param action:
        :param client:
        :param world:
        :param bot:
        :return: None
        """
    stunned = False
    # match interaction type with x and y
    vector: Vector
    match action:
        case ActionType.ATTACK_UP:
            vector = Vector(x=0, y=-1)
            stunned = True
        case ActionType.ATTACK_DOWN:
            vector = Vector(x=0, y=1)
            stunned = True
        case ActionType.ATTACK_LEFT:
            vector = Vector(x=-1, y=0)
            stunned = True
        case ActionType.ATTACK_RIGHT:
            vector = Vector(x=1, y=0)
            stunned = True
        case ActionType.ATTACK_TOP_LEFT:
            vector = Vector(x=-1, y=-1)
            stunned = True
        case ActionType.ATTACK_BOTTOM_LEFT:
            vector = Vector(x=-1, y=1)
            stunned = True
        case ActionType.ATTACK_TOP_RIGHT:
            vector = Vector(x=1, y=-1)
            stunned = True
        case ActionType.ATTACK_BOTTOM_RIGHT:
            vector = Vector(x=1, y=1)
            stunned = True
            return
    # find result in interaction
    vector.x += client.avatar.position.x
    vector.y += client.avatar.position.y
    play: Player = world.get_top(vector)
    if play is not None and isinstance(play, Station):
        bot.attack(client.avatar)