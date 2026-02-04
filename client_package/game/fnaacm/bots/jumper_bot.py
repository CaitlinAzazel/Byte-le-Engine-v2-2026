from game.common.enums import ObjectType
from game.fnaacm.bots.bot import Bot


class JumperBot(Bot):
    def __init__(self):
        super().__init__()
        self.object_type = ObjectType.JUMPER_BOT
        self.vision_radius = 0
        self.boosted_vision_radius = 0
