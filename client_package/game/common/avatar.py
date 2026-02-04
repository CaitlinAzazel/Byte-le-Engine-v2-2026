from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.items.item import Item
from game.utils.vector import Vector


class Avatar(GameObject):
    """
    `Avatar Inventory Notes:`

        The avatar's inventory is a list of items. Each item has a quantity and a stack_size (the max amount of an
        item that can be held in a stack. Think of the Minecraft inventory).

        This upcoming example is just to facilitate understanding the concept. The Dispensing Station concept that will
        be mentioned is completely optional to implement if you desire. The Dispensing Station is used to help with the
        explanation.

        ----

        **Items:**
            Every Item has a quantity and a stack_size. The quantity is how much of the Item the player *currently* has.
            The stack_size is the max of that Item that can be in a stack. For example, if the quantity is 5, and the
            stack_size is 5 (5/5), the item cannot be added to that stack

        -----

        **Picking up items:**

            Example 1:
                ::
                When you pick up an item (which will now be referred to as picked_up_item), picked_up_item has a given
                quantity. In this case, let's say the quantity of picked_up_item is 2.

                Imagine you already have this item in your inventory (which will now be referred to as inventory_item),
                and inventory_item has a quantity of 1 and a stack_size of 10 (think of this as a fraction: 1/10).

                When you pick up picked_up_item, inventory_item will be checked.
                If picked_up_item's quantity + inventory_item < stack_size, it'll be added without issue.
                Remember, for this example: picked_up_item quantity is 2, and inventory_item quantity is 1, and
                stack_size is 10.

                    Inventory_item quantity before picking up: 1/10
                    ::
                        2 + 1 < 10 --> True
                    Inventory_item quantity after picking up: 3/10

            ----

            Example 2:
                For the next two examples, the total inventory size will be considered.

                Let's say inventory_item has quantity 4 and a stack_size of 5. Now say that picked_up_item has
                quantity 3.

                Recall: if picked_up_item's quantity + inventory_item < stack_size, it will be added without issue

                    Inventory_item quantity before picking up: 4/5
                    ::
                        3 + 4 < 5 --> False

                What do we do in this situation? If you want to add picked_up_item to inventory_item and there is an
                overflow of quantity, that is handled for you.

                Let's say that your inventory size (which will now be referred to as max_inventory_size) is 5. You
                already have inventory_item in there that has a quantity of 4 and a stack_size of 5. An image of the
                inventory is below. 'None' is used to help show the max_inventory_size. Inventory_item quantity and
                stack_size will be listed in parentheses as a fraction.
                ::
                    Inventory:
                    [
                        inventory_item (4/5),
                        None,
                        None,
                        None,
                        None
                    ]

                Now we will add picked_up_item and its quantity of 3:
                ::
                    Inventory before:
                    [
                        inventory_item (4/5),
                        None,
                        None,
                        None,
                        None
                    ]

                    3 + 4 < 5 --> False

                inventory_item (4/5) will now be inventory_item (5/5)
                picked_up_item now has a quantity of 2 instead of 3
                Since we have a surplus, we will append the same item with a quantity of 2 in the inventory.
                ::
                    The result is:
                    [
                        inventory_item (5/5),
                        inventory_item (2/5),
                        None,
                        None,
                        None
                    ]

            ----

            Example 3:
            For this last example, assume your inventory looks like this:
            ::
                [
                    inventory_item (5/5),
                    inventory_item (5/5),
                    inventory_item (5/5),
                    inventory_item (5/5),
                    inventory_item (4/5)
                ]

            You can only fit one more inventory_item into the last stack before the inventory is full.
            Let's say that picked_up_item has quantity of 3 again.
            ::
                Inventory before:
                [
                    inventory_item (5/5),
                    inventory_item (5/5),
                    inventory_item (5/5),
                    inventory_item (5/5),
                    inventory_item (4/5)
                ]

                    3 + 4 < 5 --> False

            inventory_item (4/5) will now be inventory_item (5/5)
            picked_up_item now has a quantity of 2
            However, despite the surplus, we cannot add it into our inventory, so the remaining quantity of
            picked_up_item is left where it was first found.
            ::
                Inventory after:
                [
                    inventory_item (5/5),
                    inventory_item (5/5),
                    inventory_item (5/5),
                    inventory_item (5/5),
                    inventory_item (5/5)
                ]
    """

    MAX_POWER = 100

    def __init__(self, position: Vector | None = None, max_inventory_size: int = 10):
        super().__init__()
        self.object_type: ObjectType = ObjectType.AVATAR
        self.score: int = 0
        self.position: Vector | None = position
        self.max_inventory_size: int = max_inventory_size
        self.inventory: list[Item | None] = [None] * max_inventory_size
        self.held_item: Item | None = self.inventory[0]
        self.power: int = Avatar.MAX_POWER
        self.__held_index: int = 0
        self.health: int = 3

    def give_score(self, amount: int) -> None:
        ...

    def give_power(self, amount: int) -> None:
        ...

    def add_point(self):
        ...

    def action(self):
        ...

    def receive_attack(self):
        ...

    @property
    def is_alive(self) -> bool:
        ...

    @property
    def health(self) -> int:
        return self.__health

    @health.setter
    def health(self, value: int) -> None:
        if value is None or not isinstance(value, int):
            raise TypeError(
                f'{self.__class__.__name__}.health must be an int '
                f'It is a(n) {value.__class__.__name__} and has the value of {value}')
        if value < 0:
            raise ValueError(f'{self.__class__.__name__}.health must be nonnegative; attempted to set it to {value}')
        self.__health = value

    @property
    def power(self) -> int:
        return self.__power

    @property
    def held_item(self) -> Item | None:
        self.__clean_inventory()
        return self.inventory[self.__held_index]

    @property
    def score(self) -> int:
        return self.__score

    @property
    def position(self) -> Vector | None:
        return self.__position

    @property
    def inventory(self) -> list[Item | None]:
        return self.__inventory

    @property
    def max_inventory_size(self) -> int:
        return self.__max_inventory_size

    @power.setter
    def power(self, value: int) -> None:
        if value is None or not isinstance(value, int):
            raise TypeError(
                f'{self.__class__.__name__}.score must be an int '
                f'It is a(n) {value.__class__.__name__} and has the value of {value}')
        if value < 0:
            raise ValueError(f'{self.__class__.__name__}.power must be nonnegative; attempted to set it to {value}')
        if value > Avatar.MAX_POWER:
            raise ValueError(f'{self.__class__.__name__}.power must be less than {Avatar.MAX_POWER}; attempted to set it to {value}')
        self.__power = value

    @held_item.setter
    def held_item(self, item: Item | None) -> None:
        self.__clean_inventory()

        # If it's not an item, and it's not None, raise the error
        if item is not None and not isinstance(item, Item):
            raise ValueError(
                f'{self.__class__.__name__}.held_item must be an Item or None. It is a(n) '
                f'{item.__class__.__name__} and has the value of {item}')

        # If the item is not contained in the inventory, the error will be raised.
        if not self.inventory.__contains__(item):
            raise ValueError(f'{self.__class__.__name__}.held_item must be set to an item that already exists'
                             f' in the inventory. It has the value of {item}')

        # If the item is contained in the inventory, set the held_index to that item's index
        self.__held_index = self.inventory.index(item)

    @score.setter
    def score(self, score: int) -> None:
        if score is None or not isinstance(score, int):
            raise ValueError(
                f'{self.__class__.__name__}.score must be an int. It is a(n) {score.__class__.__name__} and has the value of '
                f'{score}')
        self.__score: int = score

    @position.setter
    def position(self, position: Vector | None) -> None:
        if position is not None and not isinstance(position, Vector):
            raise ValueError(
                f'{self.__class__.__name__}.position must be a Vector or None. It is a(n) '
                f'{position.__class__.__name__} and has the value of {position}')
        self.__position: Vector | None = position

    @inventory.setter
    def inventory(self, inventory: list[Item | None]) -> None:
        # If every item in the inventory is not of type None or Item, throw an error
        if inventory is None or not isinstance(inventory, list) \
                or (len(inventory) > 0 and any(map(lambda item: item is not None and not
        isinstance(item, Item), inventory))):
            raise ValueError(
                f'{self.__class__.__name__}.inventory must be a list of Items. It is a(n) {inventory.__class__.__name__} '
                f'and has the value of {inventory}')
        if len(inventory) > self.max_inventory_size:
            raise ValueError(f'{self.__class__.__name__}.inventory size must be less than or equal to '
                             f'max_inventory_size. It has the value of {len(inventory)}')
        self.__inventory: list[Item] = inventory

    @max_inventory_size.setter
    def max_inventory_size(self, size: int) -> None:
        if size is None or not isinstance(size, int):
            raise ValueError(f'{self.__class__.__name__}.max_inventory_size must be an int. It is a(n) {size.__class__.__name__} '
                             f'and has the value of {size}')
        self.__max_inventory_size: int = size

    def drop_held_item(self) -> Item | None:
        """
        Call this method when a station is taking the held item from the avatar.

        This method can be modified more for different scenarios where the held item would be dropped
        (e.g., you make a game where being attacked forces you to drop your held item).

        If you want the held item to go somewhere specifically and not become None, that can be changed too.

        Make sure to keep clean_inventory() in this method.
        """
        ...

    def take(self, item: Item | None) -> Item | None:
        """
        To use this method, pass in an item object. Whatever this item's quantity is will be the amount subtracted from
        the avatar's inventory. For example, if the item in the inventory is has a quantity of 5 and this method is
        called with the parameter having a quantity of 2, the item in the inventory will have a quantity of 3.

        Furthermore, when this method is called and the potential item is taken away, the clean_inventory method is
        called. It will consolidate all similar items together to ensure that the inventory is clean.

        Reference test_avatar_inventory.py and the clean_inventory method for further documentation on this method and
        how the inventory is managed.

        :param item:
        :return: Item or None
        """
        ...

    def pick_up(self, item: Item | None) -> Item | None:
        ...

    def get_quantity_of_item_type(self, item_type: ObjectType) -> int:
        ...
