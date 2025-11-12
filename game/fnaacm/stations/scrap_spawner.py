from typing import Self, override
from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.map.occupiable import Occupiable
from game.fnaacm.cooldown import Cooldown
from game.fnaacm.items.scrap import Scrap
from game.utils.ldtk_json import EntityInstance
from game.utils.vector import Vector

class ScrapSpawner(Occupiable):
    """
    A tile that occasionally holds scrap (generator fuel).
    """

    TURNS_TO_RESPAWN: int = 20

    class LDtkFieldIdentifiers:
        RESPAWN_RATE = 'respawn_rate'

    def __init__(self, position: Vector = Vector(0,0), respawn_rate: int = TURNS_TO_RESPAWN) -> None:
        super().__init__()
        self.object_type: ObjectType = ObjectType.SCRAP_SPAWNER
        self.position: Vector = position
        self.__cooldown: Cooldown = Cooldown(respawn_rate)

    @classmethod
    def from_ldtk_entity(cls, entity: EntityInstance) -> Self:
        position: Vector = Vector(entity.grid[0], entity.grid[1])
        respawn_rate: int = 0
        for field in entity.field_instances:
            match field.identifier:
                case ScrapSpawner.LDtkFieldIdentifiers.RESPAWN_RATE:
                    respawn_rate = field.value
        return cls(position=position, respawn_rate=respawn_rate)

    def __eq__(self, value: object, /) -> bool:
        return \
            isinstance(value, self.__class__) and \
            self.position == value.position and \
            self.__cooldown == value.__cooldown 

    @override
    def to_json(self) -> dict:
        data = super().to_json()
        data['cooldown'] = self.__cooldown.to_json()
        data['position'] = self.position.to_json()
        return data

    @override
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.position = Vector().from_json(data['position'])
        self.__cooldown = Cooldown().from_json(data['cooldown'])
        return self

    def is_available(self) -> bool:
        return self.__cooldown.can_activate

    def tick(self) -> None:
        self.__cooldown.tick()

    def handle_turn(self, avatar: Avatar) -> None:
        if self.position != avatar.position:
            return
        if not self.__cooldown.activate():
            return
        avatar.pick_up(Scrap(quantity=1))
