from General_Bot_Commands import *
import Dumb_bot
import Jumper_Bot
import Crawler_Bot
import IAN_Bot

class Support_Bot:
    def __init__(self):
        super().__init__()
        self.turnedOn = False
        self.movement_controller: MovementController = MovementController()
        self.stun = False

    def boosting(self):
        if self.turnedOn == True:
            Dumb_bot.boosted = True
            Jumper_Bot.boosted = True
            Crawler_Bot.boosted = True
            IAN_Bot.boosted = True
        else:
            Dumb_bot.boosted = False
            Jumper_Bot.boosted = False
            Crawler_Bot.boosted = False
            IAN_Bot.boosted = False

    def action(self):
        self.boosting()