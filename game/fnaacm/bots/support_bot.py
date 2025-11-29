from game.fnaacm.bots.bot import Bot
from game.fnaacm.bots.general_bot_commands import *

class SupportBot(Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.turnedOn = False
        self.movement_controller: MovementController = MovementController()
        self.stun = False

    def turned_on(self):
        return self.turnedOn

    def flip_state(self):
        self.turnedOn = not self.turnedOn
