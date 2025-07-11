from typing_extensions import override
from game.common.game_object import GameObject
from game.common.map.occupiable import Occupiable
from game.common.enums import ObjectType

class Vent(Occupiable):
    def __init__(self):
        super().__init__()
        self.object_type: ObjectType = ObjectType.VENT

    @override
    def can_occupy(self, game_object: GameObject) -> bool:
        # TODO: also allow crawler
        return game_object.object_type == ObjectType.AVATAR
