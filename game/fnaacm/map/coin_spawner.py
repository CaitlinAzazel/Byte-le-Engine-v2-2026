from typing import Self, override
from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.map.occupiable import Occupiable
from game.fnaacm.cooldown import Cooldown
from game.fnaacm.game_object_list import GameObjectList
from game.utils.ldtk_json import EntityInstance
from game.utils.vector import Vector

class CoinSpawner(Occupiable):
    """
    A tile that occasionally holds coins which increase the player's points

    The player's avatar collects coins by walking over this tile when they are available
    """

    class LDtkFieldIdentifers:
        TURNS_TO_RESPAWN = 'turns_to_respawn'
        POINT_VALUE = 'point_value'

    def __init__(self, position: Vector = Vector(0,0), turns_to_respawn: int = 1, points: int = 0) -> None:
        super().__init__()
        self.object_type: ObjectType = ObjectType.COIN
        self.position: Vector = position
        self.points: int = points
        self.__cooldown = Cooldown(duration=turns_to_respawn)

    @classmethod
    def from_ldtk_entity(cls, entity: EntityInstance) -> Self:
        position: Vector = Vector(entity.grid[0], entity.grid[1])
        turns_to_respawn: int = -1
        for field in entity.field_instances:
            match field.identifier:
                case CoinSpawner.LDtkFieldIdentifers.TURNS_TO_RESPAWN:
                    turns_to_respawn = field.value
        return cls(position=position, turns_to_respawn=turns_to_respawn)

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, self.__class__):
            return \
                self.position == value.position and \
                self.__cooldown == value.__cooldown 
        return False

    @override
    def to_json(self) -> dict:
        data = super().to_json()
        data['cooldown'] = self.__cooldown.to_json()
        data['position'] = self.position.to_json()
        data['points'] = self.points
        return data

    @override
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.__cooldown = Cooldown().from_json(data['cooldown'])
        self.position = Vector().from_json(data['position'])
        self.points = data['points']
        return self

    @property
    def is_available(self) -> bool:
        return self.__cooldown.can_activate

    def tick(self) -> None:
        self.__cooldown.tick()

    def handle_turn(self, avatar: Avatar) -> None:
        if self.position != avatar.position:
            return
        if not self.__cooldown.activate():
            return
        avatar.give_score(self.points)

class CoinSpawnerList(GameObjectList[CoinSpawner]):
    def __init__(self):
        super().__init__('coins', CoinSpawner)
