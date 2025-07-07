
from typing import Self, override
from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.items.item import Item
from game.common.stations.station import Station
from game.fnaacm.items.scrap import Scrap


class Generator(Station):
    """
    opens doors once fed scrap via interaction
    """
    def __init__(self, held_item: Item | None = None, cost: int = 1, doors: list[GameObject] = []):
        super().__init__(held_item=held_item)
        self.object_type: ObjectType = ObjectType.GENERATOR
        self.cost: int = cost
        self.connected_doors: list[GameObject] = doors # TODO: change to door class type
        self.__activated: bool = False

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

    @override
    def take_action(self, avatar: Avatar) -> Item | None:
        if self.activated:
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
        self.__activated = True
        self.__toggle_doors(True)

    @property
    def activated(self):
        return self.__activated

    def __toggle_doors(self, open: bool):
        for door in self.connected_doors:
            # TODO: open the door
            ...

