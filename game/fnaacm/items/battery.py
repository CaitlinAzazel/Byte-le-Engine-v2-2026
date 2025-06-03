from game.common.enums import ObjectType
from game.common.items.item import Item

class Battery(Item):
    """
    An collectible that the player avatar can collect to replenish power.
    """
    def __init__(self) -> None:
        super().__init__()
        self.object_type = ObjectType.BATTERY
