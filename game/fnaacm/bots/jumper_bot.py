import random
from typing import override

# from game.fnaacm.bots.general_bot_commands import *
# from game.common.map.game_board import GameBoard
from game.common.enums import ObjectType
from game.fnaacm.bots.bot import Bot

class JumperBot(Bot):
    def __init__(self):
        super().__init__()
        self.object_type = ObjectType.JUMPER_BOT
        self.vision_radius = 6
        self.boosted_vision_radius = 10
        self.stun = False
        self.cooldown = 0
