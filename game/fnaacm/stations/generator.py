
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
        self.cost = cost
        self.__scrap = Scrap(quantity=self.cost)

    def take_action(self, avatar: Avatar) -> Item | None:
        total_scrap = sum(map(lambda item: isinstance(item, Scrap), avatar.inventory))
        if total_scrap < self.cost:
            return
        avatar.take(self.__scrap)
