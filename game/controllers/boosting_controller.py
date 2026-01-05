from game.fnaacm.bots.jumper_bot import JumperBot
from game.fnaacm.bots.ian_bot import IANBot
from game.fnaacm.bots.support_bot import SupportBot
from game.fnaacm.bots.dumb_bot import DumbBot
from game.fnaacm.bots.crawler_bot import CrawlerBot
from game.controllers.controller import Controller

class BoostingController(Controller):

    def __init__(self, supportBot: SupportBot, jumperBot: JumperBot, dumbBot: DumbBot, crawlerBot: CrawlerBot, ianBot: IANBot):
        super().__init__()
        self.jumperBot = jumperBot
        self.supportBot = supportBot
        self.ianBot = ianBot
        self.crawlerBot = crawlerBot
        self.dumbBot = dumbBot

    def boosting(self):
        if self.supportBot.turned_on:
            self.jumperBot.boosting(True)
            self.dumbBot.boosting(True)
            self.crawlerBot.boosting(True)
            self.ianBot.boosting(True)
        else:
            self.jumperBot.boosting(False)
            self.dumbBot.boosting(False)
            self.crawlerBot.boosting(False)
            self.ianBot.boosting(False)


