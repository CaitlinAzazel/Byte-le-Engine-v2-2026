from typing import override
from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.stations.occupiable_station import OccupiableStation
from game.common.items.item import Item
from game.utils.vector import Vector


class BatteryOccupiableStation(OccupiableStation):
    """
    A tile that occasionally holds batteries which increase the player avatar's power.
    """
    def __init__(self, position: Vector = Vector(0,0), cooldown: int = 10) -> None:
        super().__init__()
        self.object_type = ObjectType.BATTERY
        self.position: Vector = position
        self.__battery_recharge_amount: int = 0
        # how many turns before another battery respawns after one is taken
        self.__cooldown_length: int = cooldown
        # the most recent turn a battery was taken
        # initialization to negative cd length allows player's avatar to pick up battery on turn 0 (theoretically)
        self.__battery_taken_turn: int = -self.__cooldown_length

    @override
    def take_action(self, avatar: Avatar) -> Item | None:
        if self.position != avatar.position:
            return None

        # FIXME: need to access turn this action is being taken on
        current_turn = 0
        if current_turn - self.__battery_taken_turn < self.__cooldown_length:
            return None

        avatar.power += self.__battery_recharge_amount
        self.__battery_taken_turn = current_turn
