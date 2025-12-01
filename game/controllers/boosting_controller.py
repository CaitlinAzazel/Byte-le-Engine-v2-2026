from game.fnaacm.bots.jumper_bot import JumpBot
from game.fnaacm.bots.ian_bot import IANBot
from game.fnaacm.bots.support_bot import SupportBot
from game.fnaacm.bots.dumb_bot import DumbBot
from game.fnaacm.bots.crawler_bot import CrawlerBot
from game.controllers.controller import Controller

class BoostingController(Controller):

    def __init__(self, supportBot: SupportBot, jumpBot: JumpBot, dumbBot: DumbBot, crawlerBot: CrawlerBot, ianBot: IANBot):
        super().__init__()
        self.jumpBot = jumpBot
        self.supportBot = supportBot
        self.ianBot = ianBot
        self.crawlerBot = crawlerBot
        self.dumbBot = dumbBot

    def boosting(self):
        if self.supportBot.turned_on:
            self.jumpBot.boosting(True)
            self.dumbBot.boosting(True)
            self.crawlerBot.boosting(True)
            self.ianBot.boosting(True)
        else:
            self.jumpBot.boosting(False)
            self.dumbBot.boosting(False)
            self.crawlerBot.boosting(False)
            self.ianBot.boosting(False)


