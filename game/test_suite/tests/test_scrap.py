import unittest

from game.common.enums import ObjectType
from game.fnaacm.items.scrap import Scrap


class TestScrap(unittest.TestCase):
    def setUp(self) -> None:
        self.scrap: Scrap = Scrap()

    def test_correct_object_type(self) -> None:
        self.assertEqual(self.scrap.object_type, ObjectType.SCRAP)
