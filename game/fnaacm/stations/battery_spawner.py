from typing import Self, override
from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.map.occupiable import Occupiable
from game.fnaacm.timer import Timer
from game.utils.ldtk_json import EntityInstance
from game.utils.vector import Vector

class BatterySpawner(Occupiable):
    """
    A tile that occasionally holds batteries which increase the player avatar's power.
    """

    class LDtkFieldIdentifers:
        TURNS_TO_RESPAWN = 'turns_to_respawn'
        POWER_VALUE = 'power_value'

    def __init__(self, position: Vector = Vector(0, 0), turns_to_respawn: int = 1, recharge_amount: int = 0) -> None:
        super().__init__()
        self.object_type: ObjectType = ObjectType.BATTERY
        self.position: Vector = position
        self.__recharge_amount: int = recharge_amount
        self.__timer = Timer(duration=turns_to_respawn)

    @classmethod
    def from_ldtk_entity(cls, entity: EntityInstance) -> Self:
        position: Vector = Vector(entity.grid[0], entity.grid[1])
        turns_to_respawn: int = -1
        recharge_amount: int = -1
        for field in entity.field_instances:
            match field.identifier:
                case BatterySpawner.LDtkFieldIdentifers.TURNS_TO_RESPAWN:
                    turns_to_respawn = field.value
                case BatterySpawner.LDtkFieldIdentifers.POWER_VALUE:
                    recharge_amount = field.value
        return cls(position, turns_to_respawn, recharge_amount)

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, self.__class__) and \
            self.position == value.position and \
            self.__recharge_amount == value.__recharge_amount and \
            self.__timer == value.__timer 

    @override
    def to_json(self) -> dict:
        self.state = 'idle' if self.is_available else 'unavailable'
        data = super().to_json()
        data['recharge_amount'] = self.__recharge_amount
        data['timer'] = self.__timer.to_json()
        data['position'] = self.position.to_json()
        return data

    @override
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.__recharge_amount = data['recharge_amount']
        self.__timer = Timer().from_json(data['timer'])
        self.position = Vector().from_json(data['position'])
        return self

    @property
    def is_available(self) -> bool:
        return self.__timer.done

    @property
    def recharge_amount(self) -> int:
        return self.__recharge_amount

    def tick(self) -> None:
        self.__timer.tick()

    def handle_turn(self, avatar: Avatar) -> None:
        if self.position != avatar.position:
            return
        if not self.__timer.reset(force=False):
            return
        avatar.power += self.__recharge_amount
