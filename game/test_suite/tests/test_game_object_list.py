import unittest

from game.common.game_object import GameObject
from game.fnaacm.game_object_list import GameObjectList


class TestGameObjectList(unittest.TestCase):
    def setUp(self) -> None:
        self.json_key = 'asdf'
        self.game_object_list = GameObjectList(self.json_key, GameObject)

    def test_size(self):
        self.assertEqual(self.game_object_list.size(), 0)

    def test_append(self):
        self.assertEqual(self.game_object_list.size(), 0)
        quantity = 99
        for _ in range(quantity):
            self.game_object_list.append(GameObject())
        self.assertEqual(self.game_object_list.size(), quantity)

    def test_get(self):
        game_object = GameObject()
        self.game_object_list.append(game_object)
        self.assertEqual(self.game_object_list.get(0), game_object)

    def test_to_and_from_json(self):
        quantity = 67
        for _ in range(quantity):
            self.game_object_list.append(GameObject())

        data = self.game_object_list.to_json()
        new_list = GameObjectList(self.json_key, GameObject).from_json(data)

        self.assertEqual(self.game_object_list.size(), new_list.size())

        for x in range(self.game_object_list.size()):
            original_game_object = self.game_object_list.get(x)
            new_game_object = new_list.get(x)
            self.assertEqual(original_game_object.to_json(), new_game_object.to_json())
