import unittest

from game.common.action import ActionType
from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.interact_controller import InteractController
from game.controllers.power_controller import PowerController
from game.fnaacm.items.scrap import Scrap
from game.fnaacm.stations import generator
from game.fnaacm.stations.generator import Generator
from game.utils.vector import Vector


class TestPowerController(unittest.TestCase):
    def setUp(self) -> None:
        self.__decay_frequency: int = 5
        self.__decay_amount: int = 4
        self.avatar: Avatar = Avatar()
        self.avatar.inventory.append(Scrap())
        self.player: Player = Player(None, None, [], self.avatar)

        self.power_controller = PowerController(self.__decay_frequency, self.__decay_amount)
        self.no_passive_drain_power_controller = PowerController(self.__decay_frequency, 0)
        self.interact_controller = InteractController()

        self.generator = Generator()
        self.locations: dict[Vector, list[GameObject]]= {
            Vector(0,0): [self.generator, self.avatar ]
        }
        self.generator_game_board = GameBoard(1, Vector(10, 10), self.locations, False)
        self.generator_game_board.generate_map()

        self.blank_game_board: GameBoard = GameBoard(1, Vector(10, 10), {}, False)
        self.blank_game_board.generate_map()


    # does power get drained after (frequency) turns have passed?
    def test_power_drains(self):
        starting_power = min(100, self.__decay_amount * 2)
        self.avatar.power = starting_power
        for i in range(self.__decay_frequency):
            self.power_controller.handle_actions(ActionType.NONE, self.player, self.blank_game_board)
        self.assertEqual(self.avatar.power, starting_power - self.__decay_amount)

    def test_power_drains_several_times(self):
        repetitions = 3
        starting_power = min(100, self.__decay_amount * repetitions)
        self.avatar.power = starting_power
        for i in range(self.__decay_frequency * repetitions):
            self.power_controller.handle_actions(ActionType.NONE, self.player, self.blank_game_board)
        self.assertEqual(self.avatar.power, starting_power - self.__decay_amount * repetitions)

    # does power get drained past zero?
    def test_power_drains_to_zero(self):
        self.avatar.power = self.__decay_amount - 1
        for i in range(self.__decay_frequency):
            self.power_controller.handle_actions(ActionType.NONE, self.player, self.blank_game_board)
        self.assertEqual(self.avatar.power, 0)

    # does power not get drained after (< frequency) turns have passed?
    def test_power_does_not_drain(self):
        old_power = self.avatar.power
        for i in range(self.__decay_frequency - 1):
            self.power_controller.handle_actions(ActionType.NONE, self.player, self.blank_game_board)
        self.assertEqual(self.avatar.power, old_power)

    def test_generators_drain_additional_power(self):
        starting_power = min(100, PowerController.GENERATOR_PENALTY * 2)
        self.avatar.power = starting_power
        # `self.generator.__active = True` doesn't work so the following line does that
        self.interact_controller.handle_actions(ActionType.INTERACT_CENTER, self.player, self.generator_game_board)
        for _ in range(self.__decay_frequency):
            self.no_passive_drain_power_controller.handle_actions(ActionType.NONE, self.player, self.generator_game_board)
        self.assertEqual(self.avatar.power, starting_power - PowerController.GENERATOR_PENALTY)

    def test_inactive_generators_drain_no_power(self):
        starting_power = min(100, PowerController.GENERATOR_PENALTY * 2)
        self.avatar.power = starting_power
        for _ in range(self.__decay_frequency):
            self.no_passive_drain_power_controller.handle_actions(ActionType.NONE, self.player, self.generator_game_board)
        self.assertEqual(self.avatar.power, starting_power)
