from game.common.enums import ObjectType
from game.common.items.item import Item

DEFAULT_STACK_SIZE = 10

class Scrap(Item):
    def __init__(self, value: int = 1, quantity: int = 1, stack_size: int = DEFAULT_STACK_SIZE, durability: int | None = None, ):
        super().__init__(value, durability, quantity, stack_size)
        self.object_type = ObjectType.SCRAP
