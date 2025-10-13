from typing import Self, override
from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.map.occupiable import Occupiable
from game.fnaacm.cooldown import Cooldown
from game.utils.ldtk_json import EntityInstance
from game.utils.vector import Vector

class ScrapSpawner(Occupiable):
    """
    A tile that occasionally holds scrap (generator fuel).
    """

    TURNS_TO_RESPAWN: int = 20

    def __init__(self, position: Vector = Vector(0,0)) -> None:
        super().__init__()
        self.object_type: ObjectType = ObjectType.BATTERY
        self.position: Vector = position
        self.__cooldown: Cooldown = Cooldown(ScrapSpawner.TURNS_TO_RESPAWN)

    @classmethod
    def from_ldtk_entity(cls, entity: EntityInstance) -> Self:
        position: Vector = Vector(entity.grid[0], entity.grid[1])
        return cls(position=position)

    def __eq__(self, value: object, /) -> bool:
        return \
            isinstance(value, self.__class__) and \
            self.position == value.position and \
            self.__cooldown == value.__cooldown 

    @override
    def to_json(self) -> dict:
        data = super().to_json()
        data['recharge_amount'] = self.__recharge_amount
        data['cooldown'] = self.__cooldown.to_json()
        data['position'] = self.position.to_json()
        return data

    @override
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.__recharge_amount = data['recharge_amount']
        self.__cooldown = Cooldown().from_json(data['cooldown'])
        self.position = Vector().from_json(data['position'])
        return self

    def is_available(self) -> bool:
        return self.__cooldown.can_activate

    def handle_turn(self, avatar: Avatar) -> None:
        self.__cooldown.tick()
        if self.position != avatar.position:
            return
        if not self.__cooldown.activate():
            return
        # TODO: give them scrap
