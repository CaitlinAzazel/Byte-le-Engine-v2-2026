from game.common.enums import ActionType
from game.constants import ATTACK_TO_DIRECTION, DIRECTION_TO_ATTACK
from game.controllers.controller import Controller
from game.common.player import Player
from game.common.map.game_board import GameBoard
from game.fnaacm.bots.bot import Bot
from game.common.avatar import Avatar
from game.fnaacm.bots.support_bot import SupportBot
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

    def calculate_attack_action(self, bot: Bot, avatar: Avatar) -> ActionType:
        assert avatar.position is not None
        direction = (avatar.position - bot.position).clamp_xy(-1, 1)
        return DIRECTION_TO_ATTACK[direction]

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard, bot: Bot, supportBot: SupportBot|None = None) -> None:
        bot.has_attacked = False

        if not bot.can_attack(client.avatar):
            return

        # Invalid attack type
        if action not in ATTACK_TO_DIRECTION:
            return

        base_direction = ATTACK_TO_DIRECTION[action]
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

                    if supportBot != None:
                        supportBot.turnoff()

                    bot.has_attacked = True
                    return
