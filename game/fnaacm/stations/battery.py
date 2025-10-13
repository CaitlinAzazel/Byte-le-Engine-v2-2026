from typing import Self, override
from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.map.occupiable import Occupiable
from game.fnaacm.cooldown import Cooldown
from game.utils.ldtk_json import EntityInstance
from game.utils.vector import Vector

# TODO: rename to BatterySpawn
class Battery(Occupiable):
    """
    A tile that occasionally holds batteries which increase the player avatar's power.
    """

    class LDtkFieldIdentifers:
        COOLDOWN_DURATION = 'cooldown_duration'
        RECHARGE_AMOUNT = 'recharge_amount'

    def __init__(self, position: Vector = Vector(0,0), cooldown_duration: int = 10, recharge_amount: int = 10) -> None:
        super().__init__()
        self.object_type: ObjectType = ObjectType.BATTERY
        self.position: Vector = position
        self.__recharge_amount: int = recharge_amount
        self.__cooldown = Cooldown(duration=cooldown_duration)

    @classmethod
    def from_ldtk_entity(cls, entity: EntityInstance) -> Self:
        position: Vector = Vector(entity.grid[0], entity.grid[1])
        cooldown_duration: int = -1
        recharge_amount: int = -1
        for field in entity.field_instances:
            match field.identifier:
                case Battery.LDtkFieldIdentifers.COOLDOWN_DURATION:
                    cooldown_duration = field.value
                case Battery.LDtkFieldIdentifers.RECHARGE_AMOUNT:
                    recharge_amount = field.value
        return cls(position, cooldown_duration, recharge_amount)

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, self.__class__):
            return \
                self.position == value.position and \
                self.__recharge_amount == value.__recharge_amount and \
                self.__cooldown == value.__cooldown 
        return False

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
        avatar.power += self.__recharge_amount
