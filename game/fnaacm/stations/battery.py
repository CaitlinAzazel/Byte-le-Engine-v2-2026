from typing_extensions import override

from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.map.occupiable import Occupiable
from game.common.items.item import Item
from game.common.player import Player
from game.utils.vector import Vector


class Battery(Occupiable):
    """
    A tile that occasionally holds batteries which increase the player avatar's power.
    """
    def __init__(self, position: Vector = Vector(0,0), cooldown: int = 10, recharge_amount: int = 10) -> None:
        super().__init__()
        self.object_type: ObjectType = ObjectType.BATTERY
        self.position: Vector = position
        self.__recharge_amount: int = recharge_amount
        self.__cooldown_length: int = cooldown
        self.__cooldown_timer: int = 0

    def tick(self) -> None:
        # dont really gaf if it goes negative
        self.__cooldown_timer -= 1

    def handle_turn(self, avatar: Avatar) -> None:
        if self.position != avatar.position:
            return
        if self.__cooldown_timer > 0:
            return
        avatar.power += self.__recharge_amount
        self.__cooldown_timer = self.__cooldown_length
