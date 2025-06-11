from game.common.enums import ActionType
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.controller import Controller


class PowerController(Controller):
    """
    manages the passive drain of power from the player
    """
    def __init__(self, decay_frequency: int = 5, decay_amount: int = 0):
        super().__init__()
        self.__decay_frequency: int = decay_frequency # in turns
        self.__decay_amount: int = decay_amount
        self.__decay_tick: int = 0

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard):
        del action # unused params

        # only do stuff every decay_frequency turns
        self.__decay_tick += 1
        if self.__decay_tick < self.__decay_frequency:
            return
        self.__decay_tick = 0

        client.avatar.power -= self.__decay_amount
        # access generators from world
        # generators should drain additional power