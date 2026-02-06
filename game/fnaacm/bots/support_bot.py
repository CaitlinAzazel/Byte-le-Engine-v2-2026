from typing import Self, override
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
        return self.turnedOn

    def flip_state(self):
        self.turnedOn = not self.turnedOn

    @override
    def to_json(self) -> dict:
        data = super().to_json()
        data['turnedOn'] = self.turnedOn
        return data

    @override
    def from_json(self, data: dict) -> Self:
        obj = super().from_json(data)
        obj.turnedOn = data['turnedOn']
        return obj
