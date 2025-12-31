import random
from game.fnaacm.bots.bot import Bot
from game.common.enums import ActionType, ObjectType
from game.common.map.occupiable import Occupiable
from game.controllers.controller import Controller
from game.common.map.game_board import GameBoard
from game.utils.vector import Vector


class BotMovementController(Controller):
    def __init__(self):
        super().__init__()

    @staticmethod
    def random_horizontal_move() -> ActionType:
        return random.choice([ActionType.MOVE_RIGHT, ActionType.MOVE_LEFT,])

    @staticmethod
    def random_vertical_move() -> ActionType:
        return random.choice([ActionType.MOVE_UP, ActionType.MOVE_DOWN,])

    def calc_next_moves(self, bot: Bot, world: GameBoard, turn: int) -> list[ActionType]:
        """
        :return: moves `bot` should take to get wherever it wants to go
        """
        moves = []
        if bot.is_stunned:
            return moves
        if turn % bot.turn_delay != 0:
            return moves

        if bot.can_see_player:
            # path to them
            ...
        # path to patrol
        # dumb: random n/e/s/w
        # crawler: nothing
        # ian: nothing
        # jumper: random diagonal
        # support: nothing

    def handle_actions(self, action: ActionType, bot: Bot, world: GameBoard, turn: int):
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

