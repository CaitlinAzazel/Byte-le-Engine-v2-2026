
import unittest

from game.fnaacm.cooldown import Cooldown


class TestCooldown(unittest.TestCase):
    def setUp(self) -> None:
        self.__duration = 99
        self.cooldown = Cooldown(self.__duration)
        
    def test_cooldown_goes_on_cooldown(self):
        self.cooldown.activate()
        self.assertFalse(self.cooldown.can_activate)

    def test_cooldown_state_over_time(self):
        self.assertTrue(self.cooldown.can_activate)
        self.cooldown.activate()
        for i in range(self.__duration):
            self.assertFalse(self.cooldown.can_activate)
            self.cooldown.tick()
            if i == self.__duration:
                self.assertTrue(self.cooldown.can_activate)
