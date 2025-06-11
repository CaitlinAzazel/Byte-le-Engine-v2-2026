import unittest

from game.common.action import ActionType
from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.common.stations.occupiable_station import OccupiableStation
from game.common.stations.occupiable_station_example import OccupiableStationExample
from game.common.stations.station import Station
from game.common.stations.station_example import StationExample
from game.common.stations.station_receiver_example import StationReceiverExample
from game.controllers.power_controller import PowerController
from game.utils.vector import Vector


class TestPowerController(unittest.TestCase):
    def setUp(self) -> None:
        self.__decay_frequency: int = 5
        self.__decay_amount: int = 4
        self.__starting_power: int = 10
        self.power_controller: PowerController = PowerController(self.__decay_frequency, self.__decay_amount)
        self.avatar: Avatar = Avatar()
        self.avatar.power = self.__starting_power
        self.player: Player = Player(None, None, [], self.avatar)

        # TODO: test drain caused by generators
        self.occupiable_station: OccupiableStation = OccupiableStation()
        self.station_example: StationExample = StationExample()
        self.occupiable_station_example = OccupiableStationExample()
        self.locations: dict[Vector, list[GameObject]] = {
            Vector(1, 1): [Station(None)],
            Vector(5, 4): [self.occupiable_station_example],
            Vector(6, 5): [self.station_example],
            Vector(4, 5): [StationReceiverExample()],
            Vector(5, 5): [self.avatar],
        }
        self.game_board: GameBoard = GameBoard(1, Vector(10, 10), self.locations, False)
        self.game_board.generate_map()

    # does power get drained after (frequency) turns have passed?
    def test_power_drains(self):
        for i in range(self.__decay_frequency):
            self.power_controller.handle_actions(ActionType.NONE, self.player, self.game_board)
        self.assertEqual(self.avatar.power, self.__starting_power - self.__decay_amount)

    # does power not get drained after (< frequency) turns have passed?
    def test_power_does_not_drain(self):
        for i in range(self.__decay_frequency-1):
            self.power_controller.handle_actions(ActionType.NONE, self.player, self.game_board)
        self.assertEqual(self.avatar.power, self.__starting_power)
