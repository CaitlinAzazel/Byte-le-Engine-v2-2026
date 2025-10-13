import unittest

from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.fnaacm.stations.scrap_spawner import ScrapSpawner
from game.utils.vector import Vector


class TestScrapSpawner(unittest.TestCase):
    def setUp(self) -> None:
        position = Vector()

        self.avatar: Avatar = Avatar(position = position)
        self.far_avatar: Avatar = Avatar(position = Vector(1, 1))
        self.late_avatar: Avatar = Avatar(position = position)

        self.scrap_spawner: ScrapSpawner = ScrapSpawner(
            position=position,
        )

    def test_gives_scrap(self):
        self.assertEqual(self.avatar.get_quantity_of_item_type(ObjectType.SCRAP), 0)
        self.scrap_spawner.handle_turn(self.avatar)
        self.assertEqual(self.avatar.get_quantity_of_item_type(ObjectType.SCRAP), 1)

    def test_doesnt_give_if_not_on_tile(self):
        self.assertEqual(self.far_avatar.get_quantity_of_item_type(ObjectType.SCRAP), 0)
        self.scrap_spawner.handle_turn(self.far_avatar)
        self.assertEqual(self.far_avatar.get_quantity_of_item_type(ObjectType.SCRAP), 0)

    def test_cooldown_prevents_pick_up(self):
        self.assertEqual(self.avatar.get_quantity_of_item_type(ObjectType.SCRAP), 0)
        self.assertEqual(self.late_avatar.get_quantity_of_item_type(ObjectType.SCRAP), 0)
        self.scrap_spawner.handle_turn(self.avatar)
        self.scrap_spawner.handle_turn(self.late_avatar)
        self.assertEqual(self.avatar.get_quantity_of_item_type(ObjectType.SCRAP), 1)
        self.assertEqual(self.late_avatar.get_quantity_of_item_type(ObjectType.SCRAP), 0)

    def test_gives_several_scrap(self):
        repetitions = 3
        total_turns = ((ScrapSpawner.TURNS_TO_RESPAWN + 1) * repetitions) + 1
        for i in range(total_turns):
            self.scrap_spawner.handle_turn(self.avatar)
            expected = (i // ScrapSpawner.TURNS_TO_RESPAWN) + 1
            self.assertEqual(self.avatar.get_quantity_of_item_type(ObjectType.SCRAP), expected, f'failed on turn {i}')

    def test_cooldown_activates(self):
        self.scrap_spawner.handle_turn(self.avatar)
        self.assertFalse(self.scrap_spawner.is_available())

    def test_to_and_from_json(self):
        json = self.scrap_spawner.to_json()
        new_instance = ScrapSpawner().from_json(json)
        self.assertEqual(self.scrap_spawner, new_instance)


