from General_Bot_Commands import *
import Dumb_bot
import Jumper_Bot

class Support_Bot:
    def __init__(self):
        super().__init__()
        self.turnedOn = False
        self.movement_controller: MovementController = MovementController()
        self.stun = False

    def boosting(self):
        while self.turnedOn == True:
            Dumb_bot.boosted = True
            Jumper_Bot.boosted = True

    def action(self):
        self.boosting()