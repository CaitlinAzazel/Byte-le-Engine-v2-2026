import unittest

from game.fnaacm.bots.support_bot import SupportBot


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.supportBot = SupportBot()

    def test_init(self):
        self.assertEqual(self.supportBot.turnedOn, False)
        self.assertEqual(self.supportBot.stun, False)
        self.assertEqual(self.supportBot.stun_counter, 0)

    def test_turnedOn_method_returns_correct_value(self):
        self.assertFalse(self.supportBot.turned_on())
        self.supportBot.turnedOn = True
        self.assertTrue(self.supportBot.turned_on())

    def test_flip_state(self):
        self.supportBot.turnedOn = False
        self.supportBot.flip_state()
        self.assertTrue(self.supportBot.turnedOn)

    def test_player_hit_stun(self):
        self.supportBot.player_hit_stun()
        self.assertTrue(self.supportBot.stun)
        self.assertEqual(self.supportBot.stun_counter, 5)
        self.assertFalse(self.supportBot.turnedOn)

    def test_double_player_stun(self):
        self.supportBot.player_hit_stun()
        self.assertTrue(self.supportBot.stun)
        self.assertEqual(self.supportBot.stun_counter, 5)
        self.assertFalse(self.supportBot.turnedOn)
        self.supportBot.player_hit_stun()
        self.assertTrue(self.supportBot.stun)
        self.assertEqual(self.supportBot.stun_counter, 10)
        self.assertFalse(self.supportBot.turnedOn)

    def test_scrap_stun(self):
        self.supportBot.scrap_stun()
        self.assertTrue(self.supportBot.stun)
        self.assertEqual(self.supportBot.stun_counter, 25)
        self.assertFalse(self.supportBot.turnedOn)

    def test_double_scrap_stun(self):
        self.supportBot.scrap_stun()
        self.assertTrue(self.supportBot.stun)
        self.assertEqual(self.supportBot.stun_counter, 25)
        self.assertFalse(self.supportBot.turnedOn)
        self.supportBot.scrap_stun()
        self.assertTrue(self.supportBot.stun)
        self.assertEqual(self.supportBot.stun_counter, 25)
        self.assertFalse(self.supportBot.turnedOn)

    def test_player_stun_then_scrap_stun(self):
        self.supportBot.player_hit_stun()
        self.supportBot.scrap_stun()
        self.assertTrue(self.supportBot.stun)
        self.assertEqual(self.supportBot.stun_counter, 25)
        self.assertFalse(self.supportBot.turnedOn)

    def test_scrap_stun_then_player_stun(self):
        self.supportBot.scrap_stun()
        self.supportBot.player_hit_stun()
        self.assertTrue(self.supportBot.stun)
        self.assertEqual(self.supportBot.stun_counter, 30)
        self.assertFalse(self.supportBot.turnedOn)

    def test_action_not_stunned(self):
        self.supportBot.turnedOn = True
        self.assertEqual(self.supportBot.stun, False)
        self.supportBot.action()
        self.assertEqual(self.supportBot.turnedOn, True)
        self.assertEqual(self.supportBot.stun, False)
        self.assertEqual(self.supportBot.stun_counter, 0)

    def test_action_stunned(self):
        self.supportBot.turnedOn = False
        self.supportBot.stun = True
        self.supportBot.stun_counter = 5
        self.supportBot.action()
        self.assertFalse(self.supportBot.turnedOn)
        self.assertEqual(self.supportBot.stun, True)
        self.assertEqual(self.supportBot.stun_counter, 4)

    def test_action_un_stun(self):
        self.supportBot.turnedOn = False
        self.supportBot.stun = True
        self.supportBot.stun_counter = 1
        self.supportBot.action()
        self.assertTrue(self.supportBot.turnedOn)
        self.assertEqual(self.supportBot.stun, False)
        self.assertEqual(self.supportBot.stun_counter, 0)