import unittest
from game.utils.helpers import clamp


class TestHelpers(unittest.TestCase):
    def test_clamp_below(self):
        self.assertEqual(clamp(-100, -1, 2026), -1)

    def test_clamp_above(self):
        self.assertEqual(clamp(2027, -1, 2026), 2026)

    def test_clamp_inside(self):
        self.assertEqual(clamp(67, -1, 2026), 67)
