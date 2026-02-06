from game.common.enums import ActionType
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.controller import Controller
from game.fnaacm.timer import Timer


class PowerController(Controller):
    """
    manages the passive drain of power from the player
    """

    GENERATOR_PENALTY = 0

    def __init__(self, passive_decay_frequency: int = 1, passive_decay_amount: int = 1):
        super().__init__()
        self.__passive_decay_amount = passive_decay_amount
        self.__passive_decay_cooldown: Timer = Timer(passive_decay_frequency)
        self.__generator_decay_cooldown: Timer = Timer(passive_decay_frequency)

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard):
        del action # unused params

        self.__passive_decay_cooldown.tick()
        self.__generator_decay_cooldown.tick()

        if client.avatar.power <= 0:
            return

        amount_to_take = 0

        if self.__passive_decay_cooldown.reset(force=False):
            amount_to_take += self.__passive_decay_amount

        if self.__generator_decay_cooldown.reset(force=False):
            for _, generator in world.generators.items():
                if not generator.active:
                    continue
                amount_to_take += PowerController.GENERATOR_PENALTY

        if amount_to_take == 0:
            return

        client.avatar.power -= min(client.avatar.power, amount_to_take)
