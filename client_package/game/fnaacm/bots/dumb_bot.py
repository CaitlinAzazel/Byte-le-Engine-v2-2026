from game.common.enums import ObjectType
from game.fnaacm.bots.general_bot_commands import *
from game.fnaacm.bots.bot import Bot


class DumbBot(Bot):
    def __init__(self):
        super().__init__()
        self.object_type = ObjectType.DUMB_BOT
        self.vision_radius = 0
        self.boosted_vision_radius = 0
