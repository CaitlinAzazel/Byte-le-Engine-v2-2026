from game.fnaacm.bots.bot import Bot
from game.fnaacm.bots.General_Bot_Commands import *

class SupportBot(Bot):
    def __init__(self):
        super().__init__()
        self.turnedOn = False
        self.movement_controller: MovementController = MovementController()
        self.stun = False

    def turned_on(self):
        return self.turnedOn

    def flip_state(self):
        self.turnedOn = not self.turnedOn
