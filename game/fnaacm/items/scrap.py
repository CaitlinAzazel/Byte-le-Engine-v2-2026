from game.common.enums import ObjectType
from game.common.items.item import Item


class Scrap(Item):
    def __init__(self, value: int = 1, quantity: int = 1, stack_size: int = 1, durability: int | None = None, ):
        super().__init__(value, durability, quantity, stack_size)
        self.object_type = ObjectType.ITEM
