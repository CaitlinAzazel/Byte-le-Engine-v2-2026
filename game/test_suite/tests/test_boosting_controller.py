import unittest
from game.common.botcommands.Jumper_Bot import JumpBot
from game.common.botcommands.IAN_Bot import IANBot
from game.common.botcommands.Support_bot import SupportBot
from game.common.botcommands.Dumb_bot import DumbBot
from game.common.botcommands.Crawler_Bot import CrawlBot
from game.controllers.boosting_controller import BoostingController


class TestCaseA(unittest.TestCase):
    def setUp(self):
        self.boosting_controller: BoostingController = BoostingController()
        self.jumpBot = JumpBot()
        self.supportBot = SupportBot()
        self.ianBot = IANBot()
        self.crawlerBot = CrawlBot()
        self.dumbBot = DumbBot()

    def test_boosting_turned_off(self):
        self.supportBot.turned_on = False
        print(self.crawlerBot.boosted)
        print(self.dumbBot.boosted)
        print(self.jumpBot.boosted)
        print(self.ianBot.boosted)
        self.boosting_controller.boosting()
        print(self.crawlerBot.boosted)
        print(self.dumbBot.boosted)
        print(self.jumpBot.boosted)
        print(self.ianBot.boosted)

    def test_boosting_turned_on(self):
        self.supportBot.turned_on = True
        print(self.crawlerBot.boosted)
        print(self.dumbBot.boosted)
        print(self.jumpBot.boosted)
        print(self.ianBot.boosted)
        self.boosting_controller.boosting()
        print(self.crawlerBot.boosted)
        print(self.dumbBot.boosted)
        print(self.jumpBot.boosted)
        print(self.ianBot.boosted)

    def test_boosting_start_off_turn_on_off_on(self):
        print(self.crawlerBot.boosted)
        print(self.dumbBot.boosted)
        print(self.jumpBot.boosted)
        print(self.ianBot.boosted)
        self.supportBot.turned_on = True
        self.boosting_controller.boosting()
        print(self.crawlerBot.boosted)
        print(self.dumbBot.boosted)
        print(self.jumpBot.boosted)
        print(self.ianBot.boosted)
        self.supportBot.turned_on = False
        self.boosting_controller.boosting()
        print(self.crawlerBot.boosted)
        print(self.dumbBot.boosted)
        print(self.jumpBot.boosted)
        print(self.ianBot.boosted)
        self.supportBot.turned_on = True
        self.boosting_controller.boosting()
        print(self.crawlerBot.boosted)
        print(self.dumbBot.boosted)
        print(self.jumpBot.boosted)
        print(self.ianBot.boosted)