from typing import Self, override
from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.map.occupiable import Occupiable
from game.fnaacm.items.scrap import Scrap
from game.fnaacm.timer import Timer
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
        self.__timer: Timer = Timer(turns_to_respawn)

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
            self.__timer == value.__timer 

    @override
    def to_json(self) -> dict:
        self.state = 'idle' if self.is_available else 'unavailable'
        data = super().to_json()
        data['timer'] = self.__timer.to_json()
        data['position'] = self.position.to_json()
        return data

    @override
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.position = Vector().from_json(data['position'])
        self.__timer = Timer().from_json(data['timer'])
        return self

    @property
    def is_available(self) -> bool:
        return self.__timer.done

    def tick(self) -> None:
        self.__timer.tick()

    def handle_turn(self, avatar: Avatar) -> None:
        if self.position != avatar.position:
            return
        if not self.__timer.reset(force=False):
            return
        avatar.pick_up(Scrap(quantity=1))
