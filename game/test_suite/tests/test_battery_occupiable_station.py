import unittest

from game.common.stations.occupiable_station import OccupiableStation
from game.common.stations.station import Station
from game.common.map.wall import Wall
from game.common.avatar import Avatar
from game.common.items.item import Item
from game.common.enums import ObjectType
import game.test_suite.utils
from game.fnaacm.stations.battery_occupiable_station import BatteryOccupiableStation
from game.utils.vector import Vector


class TestBatteryOccupiableStation(unittest.TestCase):
    def setUp(self) -> None:
        position = Vector()

        self.__starting_power: int = 7
        self.avatar: Avatar = Avatar(position=position)
        self.avatar.power = self.__starting_power

        self.__battery_cooldown: int = 11
        self.__battery_recharge_amount: int = 4
        self.battery: BatteryOccupiableStation = BatteryOccupiableStation(
            position=position,
            cooldown=self.__battery_cooldown,
            recharge_amount=self.__battery_recharge_amount
        )
        self.utils = game.test_suite.utils

    def test_battery_occupiable_station_gives_battery(self):
        self.battery.take_action(self.avatar)
        self.assertEqual(self.avatar.power, self.__starting_power + self.__battery_recharge_amount)

    def test_battery_occupiable_station_gives_several_batteries(self):

        self.assertEqual(True, False, "go fix the FIXME in BatteryOccupiableStation.take_action")

        repetitions = 3
        total_turns = ((self.__battery_cooldown+1)*repetitions)+1
        for i in range(total_turns):
            # TODO: give OccupiableStations access to turn that action occurs on
            self.battery.take_action(self.avatar)

            # only test on turns where a battery is available
            if i % (self.__battery_cooldown+1) != 0:
                continue

            total_power = self.__starting_power + (i // self.__battery_cooldown) * self.__battery_recharge_amount
            self.assertEqual(self.avatar.power, total_power, f'failed on turn {i}')
            # we picked up another battery; check the accumulated power
