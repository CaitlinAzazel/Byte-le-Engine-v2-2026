from typing import List, Optional, override
from game.fnaacm.bots.bot import Bot
from game.common.enums import ActionType, ObjectType
from game.utils.vector import Vector
from game.controllers.pathfind_controller import a_star_path


class IANBot(Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object_type = ObjectType.IAN_BOT
        self.turn_delay = 2  # moves every 2 turns
        self.vision_radius = 20
        self.boosted_vision_radius = 30
