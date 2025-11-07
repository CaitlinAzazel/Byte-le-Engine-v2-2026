import unittest

from game.common.avatar import Avatar
from game.common.items.item import Item
import game.test_suite.utils


class TestAvatarInventory(unittest.TestCase):
    """
    `Test Avatar Inventory Notes:`

        This class tests the different methods in the Avatar class related to the inventory system. This is its own
        file since the inventory system has a lot of functionality. Look extensively at the different cases that are
        tested to better understand how it works if there is still confusion.
    """

    def setUp(self) -> None:
        self.avatar: Avatar = Avatar(None, 1)
        self.item: Item = Item(10, 100, 1, 1)
        self.utils = game.test_suite.utils

    # test set inventory
    def test_avatar_set_inventory(self):
        self.avatar.inventory = [Item(1, 1)]
        self.assertEqual(self.avatar.inventory[0].value, Item(1, 1).value)

    # fails if inventory is not a list
    def test_avatar_set_inventory_fail_1(self):
        value: str = 'Fail'
        with self.assertRaises(ValueError) as e:
            self.avatar.inventory = value
        self.assertTrue(
            self.utils.spell_check(str(e.exception), f'Avatar.inventory must be a list of Items. It is a(n) '
                                                     f'{value.__class__.__name__} and has the value of {value}', False))

    # fails if inventory size is greater than the max_inventory_size
    def test_avatar_set_inventory_fail_2(self):
        value: list = [Item(1, 1), Item(4, 2)]
        with self.assertRaises(ValueError) as e:
            self.avatar.inventory = value
        self.assertTrue(self.utils.spell_check(str(e.exception), 'Avatar.inventory size must be less than or equal to '
                                                                 f'max_inventory_size. It has the value of {len(value)}',
                                               False))

    def test_avatar_set_max_inventory_size(self):
        self.avatar.max_inventory_size = 10
        self.assertEqual(str(self.avatar.max_inventory_size), str(10))

    def test_avatar_set_max_inventory_size_fail(self):
        value: str = 'Fail'
        with self.assertRaises(ValueError) as e:
            self.avatar.max_inventory_size = value
        self.assertTrue(self.utils.spell_check(str(e.exception), f'Avatar.max_inventory_size must be an int. '
                                                                 f'It is a(n) {value.__class__.__name__} and has the '
                                                                 f'value of {value}', False))

    # Tests picking up an item
    def test_avatar_pick_up(self):
        self.avatar.pick_up(self.item)
        self.assertEqual(self.avatar.inventory[0], self.item)

    # Tests that picking up an item successfully returns None
    def test_avatar_pick_up_return_none(self):
        returned: Item | None = self.avatar.pick_up(self.item)
        self.assertEqual(returned, None)

    # Tests that picking up an item of one that already exists in the inventory works
    def test_avatar_pick_up_extra(self):
        item1: Item = Item(10, None, 1, 3)
        item2: Item = Item(10, None, 1, 3)
        item3: Item = Item(10, None, 1, 3)
        self.avatar.pick_up(item1)
        self.avatar.pick_up(item2)
        self.avatar.pick_up(item3)
        self.assertEqual(self.avatar.held_item.quantity, 3)

    # Tests that picking up an item that would cause a surplus doesn't cause quantity to go over stack_size
    def test_avatar_pick_up_surplus(self):
        item1: Item = Item(10, None, 2, 3)
        item2: Item = Item(10, None, 1, 3)
        item3: Item = Item(10, None, 3, 3)
        self.avatar.pick_up(item1)
        self.avatar.pick_up(item2)
        surplus: Item = self.avatar.pick_up(item3)
        self.assertEqual(self.avatar.held_item.quantity, 3)
        self.assertEqual(surplus, item3)

    # Tests when an item is being taken away
    def test_take(self):
        """
        `Take method test:`
            When this test is performed, it works properly, but because the Item class is used and is very generic, it
            may not seem to be the case. However, it does work in the end. The first item in the inventory has its
            quantity decrease to 2 after the take method is executed. Then, the helper method, clean_inventory,
            consolidates all similar Items with each other. This means that inventory[1] will add its quantity to
            inventory[0], making it have a quantity of 5; inventory[1] now has a quantity of 4 instead of 7. Then,
            inventory[2] will add its quantity to inventory[1], making it have a quantity of 7; inventory[2] now has a
            quantity of 7.

            -----

            To recap:
            When the take method is used, it will work properly with more specific Item classes being created to
            consolidate the same Item object types together

            -----

            When more subclasses of Item are created, more specific tests can be created if needed.
        """

        self.avatar: Avatar = Avatar(None, 3)
        self.avatar.inventory = [Item(quantity=5, stack_size=5), Item(quantity=7, stack_size=7),
                                 Item(quantity=10, stack_size=10)]
        taken = self.avatar.take(Item(quantity=3, stack_size=3))

        self.assertEqual(taken, None)
        self.assertEqual(self.avatar.inventory[2].quantity, 7)

    # Tests when the None value is being taken away
    def test_take_none(self):
        taken = self.avatar.take(None)
        self.assertEqual(taken, None)

    def test_take_fail(self):
        self.avatar: Avatar = Avatar(None, 3)
        self.avatar.inventory = [Item(quantity=5, stack_size=5), Item(quantity=7, stack_size=7),
                                 Item(quantity=10, stack_size=10)]
        value: str = 'wow'
        with self.assertRaises(ValueError) as e:
            taken = self.avatar.take(value)
        self.assertTrue(self.utils.spell_check(str(e.exception), f'str.item must be an item.'
                                                                 f' It is a(n) {value.__class__.__name__} with the '
                                                                 f'value of {value}.', False))

    # Tests picking up an item and failing
    def test_avatar_pick_up_full_inventory(self):
        self.avatar.pick_up(self.item)

        # Pick up again to test
        returned: Item | None = self.avatar.pick_up(self.item)
        self.assertEqual(returned, self.item)

    # Tests dropping the held item
    def test_avatar_drop_held_item(self):
        self.avatar.pick_up(self.item)
        held_item = self.avatar.drop_held_item()
        self.assertEqual(held_item, self.item)

    def test_avatar_drop_held_item_none(self):
        held_item = self.avatar.drop_held_item()
        self.assertEqual(held_item, None)


    def test_correct_quantity_calculation(self):
        item = Item(quantity=2025, stack_size=2025)
        self.avatar.inventory = [item]
        self.assertEqual(self.avatar.get_quantity_of_item_type(self.item.object_type), item.quantity)
