import unittest
from game.common.botcommands.Jumper_Bot import JumpBot
from game.common.botcommands.IAN_Bot import IANBot
from game.common.botcommands.Support_bot import SupportBot
from game.common.botcommands.Dumb_bot import DumbBot
from game.common.botcommands.Crawler_Bot import CrawlBot
from game.controllers.boosting_controller import BoostingController


class TestCaseA(unittest.TestCase):
    def setUp(self):
        self.jumpBot = JumpBot()
        self.supportBot = SupportBot()
        self.ianBot = IANBot()
        self.crawlerBot = CrawlBot()
        self.dumbBot = DumbBot()
        self.boosting_controller = BoostingController(self.supportBot, self.jumpBot, self.dumbBot, self.crawlerBot, self.ianBot)

    def test_boosting_turned_off(self):
        self.supportBot.turned_on = False
        self.assertFalse(self.crawlerBot.boosted)
        self.assertFalse(self.dumbBot.boosted)
        self.assertFalse(self.jumpBot.boosted)
        self.assertFalse(self.ianBot.boosted)
        self.boosting_controller.boosting()
        self.assertFalse(self.crawlerBot.boosted)
        self.assertFalse(self.dumbBot.boosted)
        self.assertFalse(self.jumpBot.boosted)
        self.assertFalse(self.ianBot.boosted)

    def test_boosting_turned_on(self):
        self.assertFalse(self.crawlerBot.boosted)
        self.assertFalse(self.dumbBot.boosted)
        self.assertFalse(self.jumpBot.boosted)
        self.assertFalse(self.ianBot.boosted)
        self.supportBot.flip_state()
        self.boosting_controller.boosting()
        self.assertTrue(self.crawlerBot.boosted)
        self.assertTrue(self.dumbBot.boosted)
        self.assertTrue(self.jumpBot.boosted)
        self.assertTrue(self.ianBot.boosted)

    def test_boosting_start_off_turn_on_off_on(self):
        self.assertFalse(self.crawlerBot.boosted)
        self.assertFalse(self.dumbBot.boosted)
        self.assertFalse(self.jumpBot.boosted)
        self.assertFalse(self.ianBot.boosted)
        self.supportBot.flip_state()
        self.boosting_controller.boosting()
        self.assertTrue(self.crawlerBot.boosted)
        self.assertTrue(self.dumbBot.boosted)
        self.assertTrue(self.jumpBot.boosted)
        self.assertTrue(self.ianBot.boosted)
        self.supportBot.flip_state()
        self.boosting_controller.boosting()
        self.assertFalse(self.crawlerBot.boosted)
        self.assertFalse(self.dumbBot.boosted)
        self.assertFalse(self.jumpBot.boosted)
        self.assertFalse(self.ianBot.boosted)
        self.supportBot.flip_state()
        self.boosting_controller.boosting()
        self.assertTrue(self.crawlerBot.boosted)
        self.assertTrue(self.dumbBot.boosted)
        self.assertTrue(self.jumpBot.boosted)
        self.assertTrue(self.ianBot.boosted)