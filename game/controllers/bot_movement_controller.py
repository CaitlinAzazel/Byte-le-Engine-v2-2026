from game.common.bots.bot import Bot
from game.common.enums import ActionType
from game.common.game_object import GameObject
from game.controllers.controller import Controller


class BotMovementController(Controller):
    def __init__(self):
        super().__init__()

    def handle_actions(self, bot: Bot):
        """
        Noah's Note: Calculate the Bot's desired position which should return a list of movement actions,
            and then validate and process each movement action

        Import the Position of the Bot on the Gameboard
        - Define movement vectors
        - set destination variable and combine movement vectors with the current position vector
        - validate that the bot can move into a space that is occupiable
        - validate that two bots don't share the same space

        """


