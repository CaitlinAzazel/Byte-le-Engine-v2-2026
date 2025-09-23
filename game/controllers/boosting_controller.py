from game.common.botcommands.Jumper_Bot import JumpBot
from game.common.botcommands.IAN_Bot import IANBot
from game.common.botcommands.Support_bot import SupportBot
from game.common.botcommands.Dumb_bot import DumbBot
from game.common.botcommands.Crawler_Bot import CrawlBot
from game.controllers.controller import Controller

class BoostingController(Controller):

    def __init__(self):
        super().__init__()
        self.jumpBot = JumpBot()
        self.supportBot = SupportBot()
        self.ianBot = IANBot()
        self.crawlerBot = CrawlBot()
        self.dumbBot = DumbBot()

    def boosting(self):
        if SupportBot.turned_on(self.supportBot):
            self.jumpBot.boosting(True)
            self.dumbBot.boosting(True)
            self.crawlerBot.boosting(True)
            self.ianBot.boosting(True)
        else:
            self.jumpBot.boosting(False)
            self.dumbBot.boosting(False)
            self.crawlerBot.boosting(False)
            self.ianBot.boosting(False)

