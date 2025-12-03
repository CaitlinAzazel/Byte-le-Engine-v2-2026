from game.fnaacm.bots.bot import Bot
from game.common.enums import ActionType, ObjectType
from game.common.map.occupiable import Occupiable
from game.controllers.controller import Controller
from game.common.map.game_board import GameBoard
from game.utils.vector import Vector


class BotMovementController(Controller):
    def __init__(self):
        super().__init__()

    def handle_actions(self, action: ActionType, bot: Bot, world : GameBoard ):
        """
        Noah's Note: Calculate the Bot's desired position which should return a list of movement actions,
            and then validate and process each movement action

        Import the Position of the Bot on the Gameboard
        - Define movement vectors
        - set destination variable and combine movement vectors with the current position vector
        - validate that the bot can move into a space that is occupiable
        - validate that two bots don't share the same space
        """
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

        destination: Vector = bot.position + direction

        if not world.can_object_occupy(destination, bot):
            return

        world.update_object_position(destination, bot)

