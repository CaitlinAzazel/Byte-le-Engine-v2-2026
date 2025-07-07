
import unittest

from game.common.items.item import Item
from game.common.avatar import Avatar
from game.common.player import Player
from game.common.map.game_board import GameBoard
from game.controllers.interact_controller import InteractController
from game.fnaacm.items.scrap import Scrap
from game.utils.vector import Vector
from game.common.enums import ActionType
from game.fnaacm.stations.generator import Generator

class TestGenerator(unittest.TestCase):
    def setUp(self) -> None:

        position = Vector()
        self.initial_scrap = 10
        self.avatar = Avatar(position=position, max_inventory_size=self.initial_scrap)
        self.scrap = Scrap(quantity=self.initial_scrap)
        self.inventory: list[Item] = [self.scrap, ]
        self.avatar.inventory = self.inventory

        self.player = Player(avatar=self.avatar)

        self.cost: int = 3
        self.generator = Generator(cost=self.cost)
        self.game_board = GameBoard(None, Vector(4, 4), { position: [self.generator, ], }, False)
        self.game_board.generate_map()
        self.interact_controller = InteractController()

    # can the avatar interact with the generator?
    def test_take_action(self):
        self.assertGreater(self.initial_scrap, self.cost)
        self.interact_controller.handle_actions(ActionType.INTERACT_CENTER, self.player, self.game_board)
        self.assertEqual(self.scrap.quantity, self.initial_scrap - self.cost)

    # does the generator turn on when given scrap?
    def test_activates_on_interact(self):
        self.assertGreater(self.initial_scrap, self.cost)
        self.assertFalse(self.generator.active)
        self.interact_controller.handle_actions(ActionType.INTERACT_CENTER, self.player, self.game_board)
        self.assertTrue(self.generator.active)

    # does the generator stay off when a broke player tries to activate it?
    def test_not_enough_scrap(self):
        initial_scrap = self.cost - 1
        self.scrap.quantity = initial_scrap
        self.assertFalse(self.generator.active)
        self.interact_controller.handle_actions(ActionType.INTERACT_CENTER, self.player, self.game_board)
        self.assertEqual(self.scrap.quantity, initial_scrap)
        self.assertFalse(self.generator.active)

    def test_json(self):
        data: dict = self.generator.to_json()
        generator: Generator = Generator().from_json(data)
        self.assertEqual(self.generator.object_type, generator.object_type)
        self.assertEqual(self.generator.cost, generator.cost)
