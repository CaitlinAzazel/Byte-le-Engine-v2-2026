
from typing import Self, override
from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.items.item import Item
from game.common.stations.station import Station
from game.fnaacm.items.scrap import Scrap


class Generator(Station):
    """
    opens doors once fed scrap via interaction
    """
    def __init__(self, held_item: Item | None = None, cost: int = 1):
        super().__init__(held_item=held_item)
        self.object_type: ObjectType = ObjectType.GENERATOR
        self.cost: int = cost
        # self.__scrap: Scrap = Scrap(quantity=self.cost)

    def take_action(self, avatar: Avatar) -> Item | None:
        # total_scrap = sum(map(lambda item: item.quantity if isinstance(item, Scrap) else 0, avatar.inventory))
        total_scrap = 0
        for item in avatar.inventory:
            if not isinstance(item, Scrap):
                continue
            total_scrap += item.quantity
        if total_scrap < self.cost:
            return
        avatar.take(Scrap(quantity=self.cost))

    @override
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.cost = data['cost']
        return self

    @override
    def to_json(self) -> dict:
        jason = super().to_json()
        jason['cost'] = self.cost
        return jason
