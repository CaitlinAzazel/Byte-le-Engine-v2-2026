from game.common.enums import ObjectType
from game.fnaacm.bots.bot import Bot
from game.fnaacm.bots.general_bot_commands import *


class SupportBot(Bot):
    def __init__(self):
        super().__init__()
        self.object_type = ObjectType.SUPPORT_BOT
        self.turnedOn = False

    @property
    def turned_on(self):
        ...
