from game.common.enums import ActionType
from game.controllers.controller import Controller
from game.common.player import Player
from game.common.map.game_board import GameBoard
from game.fnaacm.bots.bot import Bot
from game.common.avatar import Avatar
from game.utils.vector import Vector
from game.fnaacm.map.vent import Vent

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
class Attack_Controller(Controller):

    def __init__(self):
        super().__init__()

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard, bot: Bot) -> None:
        bot.has_attacked = False

        direction = None

        match action:
            case ActionType.ATTACK_UP:
                direction = Vector(0, -1)
            case ActionType.ATTACK_DOWN:
                direction = Vector(0, 1)
            case ActionType.ATTACK_LEFT:
                direction = Vector(-1, 0)
            case ActionType.ATTACK_RIGHT:
                direction = Vector(1, 0)
            case ActionType.ATTACK_TOP_LEFT:
                direction = Vector(-1, -1)
            case ActionType.ATTACK_BOTTOM_LEFT:
                direction = Vector(-1, 1)
            case ActionType.ATTACK_TOP_RIGHT:
                direction = Vector(1, -1)
            case ActionType.ATTACK_BOTTOM_RIGHT:
                direction = Vector(1, 1)
            case _:
                return

        target_pos = bot.position + direction

        # Get whole tile stack (not just top)
        tile_stack = world.get(target_pos)

        # Attack blocked if ANY vent exists on the target tile
        if any(isinstance(obj, Vent) for obj in tile_stack):
            return

        # Attack Avatar if visible in the tile stack
        for obj in tile_stack:
            if isinstance(obj, Avatar):
                bot.attack(obj)
                bot.has_attacked = True
                return
