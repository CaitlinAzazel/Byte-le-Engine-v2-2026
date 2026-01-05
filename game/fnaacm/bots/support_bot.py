from game.fnaacm.bots.bot import Bot
from game.fnaacm.bots.general_bot_commands import *

class SupportBot(Bot):
    def __init__(self):
        super().__init__()
        self.turnedOn = False
        self.stun = False

    @property
    def turned_on(self):
        return self.turnedOn

    def flip_state(self):
        self.turnedOn = not self.turnedOn
