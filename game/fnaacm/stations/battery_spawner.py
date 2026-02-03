from typing import Self, override
from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.map.occupiable import Occupiable
from game.fnaacm.ldtk_entity import LDtkEntity
from game.fnaacm.timer import Timer
from game.utils.ldtk_json import EntityInstance
from game.utils.vector import Vector

class BatterySpawner(Occupiable, LDtkEntity):
    """
    A tile that occasionally holds batteries which increase the player avatar's power.
    """

    class LDtkFieldIdentifers:
        TURNS_TO_RESPAWN = 'turns_to_respawn'
        POWER_VALUE = 'power_value'
        POINT_VALUE = 'point_value'

    def __init__(self, position: Vector = Vector(0, 0), turns_to_respawn: int = 1, recharge_amount: int = 1, point_value: int = 1) -> None:
        super().__init__()
        self.object_type: ObjectType = ObjectType.BATTERY_SPAWNER
        self.position: Vector = position
        self.point_value: int = point_value
        self.__recharge_amount: int = recharge_amount
        self.__timer = Timer(duration=turns_to_respawn)

    @override
    @classmethod
    def from_ldtk_entity(cls, entity: EntityInstance) -> Self:
        position: Vector = Vector(entity.grid[0], entity.grid[1])
        turns_to_respawn: int = -1
        recharge_amount: int = -1
        point_value: int = -1
        for field in entity.field_instances:
            match field.identifier:
                case BatterySpawner.LDtkFieldIdentifers.TURNS_TO_RESPAWN:
                    turns_to_respawn = field.value
                case BatterySpawner.LDtkFieldIdentifers.POWER_VALUE:
                    recharge_amount = field.value
                case BatterySpawner.LDtkFieldIdentifers.POINT_VALUE:
                    point_value = field.value
        return cls(position, turns_to_respawn, recharge_amount, point_value)

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, self.__class__) and \
            self.position == value.position and \
            self.__recharge_amount == value.__recharge_amount and \
            self.__timer == value.__timer and \
            self.point_value == value.point_value

    @override
    def to_json(self) -> dict:
        self.state = 'idle' if self.is_available else 'unavailable'
        data = super().to_json()
        data['recharge_amount'] = self.__recharge_amount
        data['timer'] = self.__timer.to_json()
        data['position'] = self.position.to_json()
        data['point_value'] = self.point_value
        return data

    @override
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.__recharge_amount = data['recharge_amount']
        self.__timer = Timer().from_json(data['timer'])
        self.position = Vector().from_json(data['position'])
        self.point_value = data['point_value']
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
        avatar.give_power(self.__recharge_amount)
        avatar.give_score(self.point_value)
