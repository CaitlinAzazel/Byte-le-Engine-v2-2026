from game.common.enums import ObjectType
from game.common.game_object import GameObject
from typing import Self


class Item(GameObject):
    """
    `Item Class Notes:`

        Items have 4 different attributes: value, durability, quantity, stack-size.

        -----

        Value:
            The value of an item can be anything depending on the purpose of the game. For example, if a player can
            sell an item to a shop for monetary value, the value attribute would be used. However, this value may be
            used for anything to better fit the purpose of the game being created.

        -----

        Durability:
            The value of an item's durability can be either None or an integer.
            If durability is an integer, the stack size *must* be 1. Think of Minecraft and the mechanics of tools. You
            can only have one sword with a durability (they don't stack).

            If the durability is equal to None, it represents the item having infinite durability. The item can now be
            stacked with others of the same type. In the case the game being created needs items without durability,
            set this attribute to None to prevent any difficulties.

        -----

        Quantity and Stack Size:
            These two work in tandem. Fractions (x/y) will be used to better explain the concept.

            Quantity simply refers to the amount of the current item the player has. For example, having 5 gold, 10
            gold, or 0 gold all work for representing the quantity.

            The stack_size represents how *much* of an item can be in a stack. Think of this like the Minecraft inventory
            system. For example, you can have 64 blocks of dirt, and if you were to gain one more, you would have a new
            stack starting at 1.

            In the case of items here, it works with the avatar.py file's inventory system (refer to those notes on how
            the inventory works in depth). The Minecraft analogy should help understand the concept.

            To better show this, quantity and stack size work like the following fraction model: quantity/stack_size.

            The quantity can never be 0 and must always be a minimum of 1. Furthermore, quantity cannot be greater than
            the stack_size. So 65/64 will not be possible.

        -----

        Pick Up Method:
            When picking up an item, it will first check the item's ObjectType. If the Object interacted with is not of
            the ObjectType ITEM enum, an error will be thrown.

            Otherwise, the method will check if the picked up item will be able to fit in the inventory. If some of the
            item's quantity can be picked up and a surplus will be left over, the player will be pick up what they can.

            Then, the same item they picked up will have its quantity modified to be what is left over. That surplus of
            the item is then returned to allow for it to be placed back where it was found on the map.

            If the player can pick up an item without any inventory issues, the entire item and its quantity will be added.

        **Refer to avatar.py for a more in-depth explanation of how picking up items work with examples.**
    """

    def __init__(self, value: int = 1, durability: int | None = None, quantity: int = 1, stack_size: int = 1):
        super().__init__()
        self.__quantity = None  # This is here to prevent an error
        self.__durability = None  # This is here to prevent an error
        self.object_type: ObjectType = ObjectType.ITEM
        self.value: int = value  # Value can more specified based on purpose (e.g., the sell price)
        self.stack_size: int = stack_size  # the max quantity this item can contain
        self.durability: int | None = durability  # durability can be None to represent infinite durability
        self.quantity: int = quantity  # the current amount of this item

    @property
    def durability(self) -> int | None:
        return self.__durability

    @property
    def value(self) -> int:
        return self.__value

    @property
    def quantity(self) -> int:
        return self.__quantity

    @property
    def stack_size(self) -> int:
        return self.__stack_size

    @durability.setter
    def durability(self, durability: int | None) -> None:
        if durability is not None and not isinstance(durability, int):
            raise ValueError(
                f'{self.__class__.__name__}.durability must be an int. It is a(n) {durability.__class__.__name__} with the value of {durability}.')
        if durability is not None and self.stack_size != 1:
            raise ValueError(
                f'{self.__class__.__name__}.durability must be set to None if stack_size is not equal to 1.'
                f' {self.__class__.__name__}.durability has the value of {durability}.')
        self.__durability = durability

    @value.setter
    def value(self, value: int) -> None:
        if value is None or not isinstance(value, int):
            raise ValueError(
                f'{self.__class__.__name__}.value must be an int.'
                f' It is a(n) {value.__class__.__name__} with the value of {value}.')
        self.__value: int = value

    @quantity.setter
    def quantity(self, quantity: int) -> None:
        if quantity is None or not isinstance(quantity, int):
            raise ValueError(
                f'{self.__class__.__name__}.quantity must be an int.'
                f' It is a(n) {quantity.__class__.__name__} with the value of {quantity}.')
        if quantity < 0:
            raise ValueError(
                f'{self.__class__.__name__}.quantity must be greater than or equal to 0.'
                f' {self.__class__.__name__}.quantity has the value of {quantity}.')

        # The self.quantity is set to the lower value between stack_size and the given quantity
        # The remaining given quantity is returned if it's larger than self.quantity
        if quantity > self.stack_size:
            raise ValueError(f'{self.__class__.__name__}.quantity cannot be greater than '
                             f'{self.__class__.__name__}.stack_size.'
                             f' {self.__class__.__name__}.quantity has the value of {quantity}.')
        self.__quantity: int = quantity

    @stack_size.setter
    def stack_size(self, stack_size: int) -> None:
        if stack_size is None or not isinstance(stack_size, int):
            raise ValueError(
                f'{self.__class__.__name__}.stack_size must be an int.'
                f' It is a(n) {stack_size.__class__.__name__} with the value of {stack_size}.')
        if self.durability is not None and stack_size != 1:
            raise ValueError(f'{self.__class__.__name__}.stack_size must be 1 if {self.__class__.__name__}.durability '
                             f'is not None. {self.__class__.__name__}.stack_size has the value of {stack_size}.')
        if self.__quantity is not None and stack_size < self.__quantity:
            raise ValueError(
                f'{self.__class__.__name__}.stack_size must be greater than or equal to the quantity.'
                f' {self.__class__.__name__}.stack_size has the value of {stack_size}.')
        self.__stack_size: int = stack_size

    def take(self, item: Self) -> Self | None:
        ...

    def pick_up(self, item: Self) -> Self | None:
        ...
