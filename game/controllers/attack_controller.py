from game.common.enums import ActionType
from game.controllers.controller import Controller
from game.common.player import Player
from game.common.map.game_board import GameBoard
from game.fnaacm.bots.bot import Bot
from game.common.avatar import Avatar
from game.utils.vector import Vector
from game.fnaacm.map.vent import Vent
from game.fnaacm.bots.jumper_bot import JumperBot

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

        # Base direction map for all actions
        direction_map = {
            ActionType.ATTACK_UP: Vector(0, -1),
            ActionType.ATTACK_DOWN: Vector(0, 1),
            ActionType.ATTACK_LEFT: Vector(-1, 0),
            ActionType.ATTACK_RIGHT: Vector(1, 0),
            ActionType.ATTACK_TOP_LEFT: Vector(-1, -1),
            ActionType.ATTACK_BOTTOM_LEFT: Vector(-1, 1),
            ActionType.ATTACK_TOP_RIGHT: Vector(1, -1),
            ActionType.ATTACK_BOTTOM_RIGHT: Vector(1, 1)
        }

        # Invalid attack type
        if action not in direction_map:
            return

        base_direction = direction_map[action]
        directions_to_check = [base_direction]

        # Boosted JumperBot special case
        if isinstance(bot, JumperBot) and bot.boosted:
            if base_direction.x != 0 and base_direction.y != 0:
                directions_to_check.extend([
                    Vector(base_direction.x, 0),
                    Vector(0, base_direction.y)
                ])

        # Process Attacks
        for direction in directions_to_check:
            target_pos = bot.position + direction
            tile_stack = world.get(target_pos)

            # Vents block attacks entirely
            if any(isinstance(obj, Vent) for obj in tile_stack):
                continue

            # Attack first Avatar on stack
            for obj in tile_stack:
                if isinstance(obj, Avatar):
                    bot.attack(obj)

                    # Turn off all generators
                    for gen in world.generators.values():
                        gen.deactivate()

                    bot.has_attacked = True
                    return