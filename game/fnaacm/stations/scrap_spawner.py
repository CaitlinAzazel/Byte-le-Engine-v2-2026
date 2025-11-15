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

    class LDtkFieldIdentifiers:
        TURNS_TO_RESPAWN = 'turns_to_respawn'

    def __init__(self, position: Vector = Vector(0, 0), turns_to_respawn: int = 1) -> None:
        super().__init__()
        self.object_type: ObjectType = ObjectType.SCRAP_SPAWNER
        self.position: Vector = position
        self.__cooldown: Cooldown = Cooldown(turns_to_respawn)

    @classmethod
    def from_ldtk_entity(cls, entity: EntityInstance) -> Self:
        position: Vector = Vector(entity.grid[0], entity.grid[1])
        turns_to_respawn: int = 0
        for field in entity.field_instances:
            match field.identifier:
                case ScrapSpawner.LDtkFieldIdentifiers.TURNS_TO_RESPAWN:
                    turns_to_respawn = field.value
        return cls(position=position, turns_to_respawn=turns_to_respawn)

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, self.__class__) and \
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
