import unittest

from game.common.avatar import Avatar
from game.fnaacm.map.coin_spawner import CoinSpawner
from game.utils.vector import Vector


class TestCoinSpawner(unittest.TestCase):
    def setUp(self) -> None:
        position = Vector()

        self.__starting_points: int = 6

        self.avatar: Avatar = Avatar(position = position)
        self.avatar.score = self.__starting_points
        self.far_avatar: Avatar = Avatar(position = Vector(1,1))
        self.far_avatar.score = self.__starting_points
        self.avatar2: Avatar = Avatar(position = position)


        self.__coin_cooldown: int = 11
        self.__coin_value: int = 4
        self.coin_spawner: CoinSpawner = CoinSpawner(
            position=position,
            turns_to_respawn=self.__coin_cooldown,
            points=self.__coin_value
        )

    def test_battery_gives_battery(self):
        self.coin_spawner.handle_turn(self.avatar)
        self.assertEqual(self.avatar.score, self.__starting_points + self.__coin_value)

    def test_battery_out_of_range(self):
        self.coin_spawner.handle_turn(self.far_avatar)
        self.assertEqual(self.far_avatar.score, self.__starting_points)

    def test_battery_on_cooldown(self):
        # kind of jank way to test this but Yeah
        self.coin_spawner.handle_turn(self.avatar2)
        self.coin_spawner.handle_turn(self.avatar)
        self.assertEqual(self.avatar.score, self.__starting_points)

    def test_battery_gives_several_batteries(self):
        repetitions = 3
        total_turns = ((self.__coin_cooldown+1)*repetitions)+1
        for i in range(total_turns):
            self.coin_spawner.tick()
            self.coin_spawner.handle_turn(self.avatar)
            total_power = self.__starting_points + (i // self.__coin_cooldown + 1) * self.__coin_value
            self.assertEqual(self.avatar.score, total_power, f'failed on turn {i}')

    def test_battery_cooldown_activates(self):
        self.coin_spawner.handle_turn(self.avatar)
        self.assertFalse(self.coin_spawner.is_available)

    def test_battery_json(self):
        json = self.coin_spawner.to_json()
        new_spawner = CoinSpawner().from_json(json)
        self.assertEqual(self.coin_spawner, new_spawner)


