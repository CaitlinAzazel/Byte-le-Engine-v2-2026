import unittest

from game.common.avatar import Avatar
from game.fnaacm.stations.battery import Battery
from game.utils.vector import Vector


class TestBattery(unittest.TestCase):
    def setUp(self) -> None:
        position = Vector()

        self.__starting_power: int = 7
        self.avatar: Avatar = Avatar(position = position)
        self.avatar.power = self.__starting_power
        self.far_avatar: Avatar = Avatar(position = Vector(1,1))
        self.far_avatar.power = self.__starting_power
        self.avatar2: Avatar = Avatar(position = position)

        self.__battery_cooldown: int = 11
        self.__battery_recharge_amount: int = 4
        self.battery: Battery = Battery(
            position=position,
            cooldown=self.__battery_cooldown,
            recharge_amount=self.__battery_recharge_amount
        )

    def test_battery_gives_battery(self):
        self.battery.handle_turn(self.avatar)
        self.assertEqual(self.avatar.power, self.__starting_power + self.__battery_recharge_amount)

    def test_battery_out_of_range(self):
        self.battery.handle_turn(self.far_avatar)
        self.assertEqual(self.far_avatar.power, self.__starting_power)

    def test_battery_on_cooldown(self):
        # kind of jank way to test this but Yeah
        self.battery.handle_turn(self.avatar2)
        self.battery.handle_turn(self.avatar)
        self.assertEqual(self.avatar.power, self.__starting_power)

    def test_battery_gives_several_batteries(self):
        repetitions = 3
        total_turns = ((self.__battery_cooldown+1)*repetitions)+1
        for i in range(total_turns):
            self.battery.tick()
            self.battery.handle_turn(self.avatar)
            total_power = self.__starting_power + (i // self.__battery_cooldown + 1) * self.__battery_recharge_amount
            self.assertEqual(self.avatar.power, total_power, f'failed on turn {i}')

    def test_battery_available(self):
        self.assertTrue(self.battery.is_available)

    def test_battery_unavailable(self):
        self.battery.handle_turn(self.avatar)
        self.assertFalse(self.battery.is_available)

    def test_battery_availability_over_time(self):
        self.assertTrue(self.battery.is_available)
        self.battery.handle_turn(self.avatar)
        for i in range(self.__battery_cooldown):
            self.assertFalse(self.battery.is_available)
            self.battery.tick()
        self.assertTrue(self.battery.is_available)

