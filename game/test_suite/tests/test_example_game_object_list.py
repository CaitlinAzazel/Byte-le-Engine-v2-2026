from typing import Self
import unittest

from game.common.game_object import GameObject
from game.fnaacm.game_object_list import GameObjectList


class ExampleGameObject(GameObject):
    """
    - for testing the Generic aspect of GameObjectList
    - also boilerplate for defining GameObjectList subclasses
    """
    def __init__(self, more_data: int = 0):
        super().__init__()
        self.extra_data: str = \
            'I am new to GitHub and I have lots to say\n' \
            'I DONT GIVE A FUCK ABOUT THE FUCKING CODE! i just want to download this stupid fucking application and use it https://github.com/sherlock-project/sherlock#installation\n' \
            'WHY IS THERE CODE??? MAKE A FUCKING .EXE FILE AND GIVE IT TO ME. these dumbfucks think that everyone is a developer and understands code. well i am not and i dont understand it. I only know to download and install applications. SO WHY THE FUCK IS THERE CODE? make an EXE file and give it to me. STUPID FUCKING SMELLY NERDS'
        self.more_data: int = more_data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.extra_data = data['extra_data']
        self.more_data = data['more_data']
        return self

    def to_json(self) -> dict:
        data = super().to_json()
        data['extra_data'] = self.extra_data
        data['more_data'] = self.more_data
        return data

class ExampleGameObjectList(GameObjectList[ExampleGameObject]):
    def __init__(self):
        super().__init__('examples', ExampleGameObject)

class TestExampleGameObjectList(unittest.TestCase):
    def setUp(self) -> None:
        self.example_list = ExampleGameObjectList()
        for i in range(5):
            self.example_list.append(ExampleGameObject(i))

    def test_to_and_from_json(self):
        data: dict = self.example_list.to_json()
        deserialized_list = ExampleGameObjectList().from_json(data)

        self.assertEqual(deserialized_list.size(), self.example_list.size())
        for x in range(self.example_list.size()):
            original = self.example_list.get(x)
            clone = deserialized_list.get(x)
            self.assertEqual(original.to_json(), clone.to_json())
