import unittest
from game.fnaacm.bots.jumper_bot import JumperBot
from game.fnaacm.bots.ian_bot import IANBot
from game.fnaacm.bots.support_bot import SupportBot
from game.fnaacm.bots.dumb_bot import DumbBot
from game.fnaacm.bots.crawler_bot import CrawlerBot
from game.controllers.boosting_controller import BoostingController


class TestCaseA(unittest.TestCase):
    def setUp(self):
        self.jumperBot = JumperBot()
        self.supportBot = SupportBot()
        self.ianBot = IANBot()
        self.crawlerBot = CrawlerBot()
        self.dumbBot = DumbBot()
        self.boosting_controller = BoostingController(
            self.supportBot,
            self.jumperBot,
            self.dumbBot,
            self.crawlerBot,
            self.ianBot
        )

    def test_boosting_turned_off(self):
        # Use the internal variable, not the property
        self.supportBot.turnedOn = False

        # Before calling boosting, all bots should be off
        self.assertFalse(self.crawlerBot.boosted)
        self.assertFalse(self.dumbBot.boosted)
        self.assertFalse(self.jumperBot.boosted)
        self.assertFalse(self.ianBot.boosted)

        self.boosting_controller.boosting()

        # After calling boosting with supportBot off, all should still be off
        self.assertFalse(self.crawlerBot.boosted)
        self.assertFalse(self.dumbBot.boosted)
        self.assertFalse(self.jumperBot.boosted)
        self.assertFalse(self.ianBot.boosted)

    def test_boosting_turned_on(self):
        # Before turning on, all bots should be off
        self.assertFalse(self.crawlerBot.boosted)
        self.assertFalse(self.dumbBot.boosted)
        self.assertFalse(self.jumperBot.boosted)
        self.assertFalse(self.ianBot.boosted)

        # Turn support bot on
        self.supportBot.turnedOn = True
        self.boosting_controller.boosting()

        # Now all bots should be boosted
        self.assertTrue(self.crawlerBot.boosted)
        self.assertTrue(self.dumbBot.boosted)
        self.assertTrue(self.jumperBot.boosted)
        self.assertTrue(self.ianBot.boosted)

    def test_boosting_start_off_turn_on_off_on(self):
        # Initially off
        self.assertFalse(self.crawlerBot.boosted)
        self.assertFalse(self.dumbBot.boosted)
        self.assertFalse(self.jumperBot.boosted)
        self.assertFalse(self.ianBot.boosted)

        # Turn on
        self.supportBot.turnedOn = True
        self.boosting_controller.boosting()
        self.assertTrue(self.crawlerBot.boosted)
        self.assertTrue(self.dumbBot.boosted)
        self.assertTrue(self.jumperBot.boosted)
        self.assertTrue(self.ianBot.boosted)

        # Turn off
        self.supportBot.turnedOn = False
        self.boosting_controller.boosting()
        self.assertFalse(self.crawlerBot.boosted)
        self.assertFalse(self.dumbBot.boosted)
        self.assertFalse(self.jumperBot.boosted)
        self.assertFalse(self.ianBot.boosted)

        # Turn on again
        self.supportBot.turnedOn = True
        self.boosting_controller.boosting()
        self.assertTrue(self.crawlerBot.boosted)
        self.assertTrue(self.dumbBot.boosted)
        self.assertTrue(self.jumperBot.boosted)
        self.assertTrue(self.ianBot.boosted)
