from game.common.enums import ActionType
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.controller import Controller

GENERATOR_PENALTY = 1
GENERATOR_DRAIN_FREQUENCY = 5

class PowerController(Controller):
    """
    manages the passive drain of power from the player
    """
    def __init__(self, decay_frequency: int = 5, decay_amount: int = 0):
        super().__init__()
        self.__decay_frequency: int = decay_frequency # in turns
        self.__decay_amount: int = decay_amount
        self.__decay_tick: int = 0
        self.__generator_tick: int = 0

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard):
        del action # unused params

        # only do stuff every decay_frequency turns
        self.__decay_tick += 1
        if self.__decay_tick < self.__decay_frequency:
            return
        self.__decay_tick = 0

        # ensure power only drains to 0
        if client.avatar.power <= 0:
            return

        amount_to_take = self.__decay_amount
        for position, generator in world.generators.items():
            if not generator.active:
                continue
            amount_to_take += GENERATOR_PENALTY

        client.avatar.power -= min(client.avatar.power, self.__decay_amount)

        # TODO: access generators from world
        # for each generator: drain additional power
