
from typing import Self, override
from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.items.item import Item
from game.common.stations.station import Station
from game.fnaacm.items.scrap import Scrap
from game.fnaacm.map.door import Door


class Generator(Station):
    """
    opens doors once fed scrap via interaction
    """
    def __init__(self, held_item: Item | None = None, cost: int = 1, doors: list[Door] = []):
        super().__init__(held_item=held_item)
        self.object_type: ObjectType = ObjectType.GENERATOR
        self.connected_doors: list[Door] = doors
        self.__active: bool = False
        self.__cost: int = cost

    @override
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.__cost = data['cost']
        self.__active = data['active']
        return self

    @override
    def to_json(self) -> dict:
        jason = super().to_json()
        jason['cost'] = self.cost
        jason['active'] = self.active
        return jason

    @override
    def take_action(self, avatar: Avatar) -> Item | None:
        if self.active:
            return
        # total_scrap = sum(map(lambda item: item.quantity if isinstance(item, Scrap) else 0, avatar.inventory))
        total_scrap = 0
        for item in avatar.inventory:
            if not isinstance(item, Scrap):
                continue
            total_scrap += item.quantity
        if total_scrap < self.cost:
            return
        avatar.take(Scrap(quantity=self.cost))
        self.__active = True
        self.__toggle_doors(True)

    @property
    def active(self) -> bool:
        return self.__active

    @property
    def cost(self) -> int:
        return self.__cost

    def __toggle_doors(self, open: bool):
        for door in self.connected_doors:
            door.open = open

