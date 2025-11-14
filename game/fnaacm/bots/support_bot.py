from game.fnaacm.bots.bot import Bot
from game.fnaacm.bots.general_bot_commands import *

class SupportBot(Bot):
    def __init__(self):
        super().__init__()
        self.turnedOn = False
        self.movement_controller: MovementController = MovementController()
        self.stun = False
        self.stun_counter = 0

    def turned_on(self):
        return self.turnedOn

    def flip_state(self):
        self.turnedOn = not self.turnedOn

    def player_hit_stun(self):
        self.stun_counter += 15
        self.stun = True
        self.turnedOn = False

    def scrap_stun(self):
        self.stun_count += 5
        self.stun = True
        self.turnedOn = False

    def action(self):
        if self.stun:
            self.stun_counter -= 1
            if self.stun_counter == 0:
                self.stun = False
                self.turnedOn = True