from typing import Self, override
from game.common.enums import ObjectType
from game.fnaacm.bots.bot import Bot
from game.fnaacm.bots.general_bot_commands import *
from game.fnaacm.timer import Timer


class SupportBot(Bot):
    def __init__(self):
        super().__init__()
        self.object_type = ObjectType.SUPPORT_BOT
        self.turnedOn = False
        self.cooldown = 250

    @property
    def turned_on(self):
        return self.turnedOn

    def flip_state(self):
        self.turnedOn = not self.turnedOn

    @override
    def to_json(self) -> dict:
        data = super().to_json()
        data['turnedOn'] = self.turnedOn
        data['cooldown'] = self.cooldown
        return data

    @override
    def from_json(self, data: dict) -> Self:
        obj = super().from_json(data)
        obj.turnedOn = data['turnedOn']
        obj.cooldown = data['cooldown']
        return obj

    def tick(self):
        self.cooldown -= 1
        if self.cooldown <= 0:
            self.turnedOn = True

    def turnoff(self):
        self.turnedOn = False
        self.cooldown = 50