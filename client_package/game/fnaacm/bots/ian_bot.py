from game.fnaacm.bots.bot import Bot
from game.common.enums import ObjectType


class IANBot(Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object_type = ObjectType.IAN_BOT
        self.turn_delay = 0
        self.vision_radius = 0
        self.boosted_vision_radius = 0
