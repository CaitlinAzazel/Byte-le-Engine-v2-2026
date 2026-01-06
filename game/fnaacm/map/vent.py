from typing import Self
from typing_extensions import override

from game.fnaacm.bots.crawler_bot import CrawlerBot
from game.common.game_object import GameObject
from game.common.map.occupiable import Occupiable
from game.common.enums import ObjectType

class Vent(Occupiable):
    def __init__(self, use_door_sprite: bool = False):
        super().__init__()
        self.object_type: ObjectType = ObjectType.VENT
        self.use_door_sprite = use_door_sprite

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.use_door_sprite = data['use_door_sprite']
        return self

    def to_json(self) -> dict:
        data = super().to_json()
        data['use_door_sprite'] = self.use_door_sprite
        return data

    @override
    def can_occupy(self, game_object: GameObject) -> bool:
        return game_object.object_type == ObjectType.AVATAR or isinstance(game_object, CrawlerBot )

