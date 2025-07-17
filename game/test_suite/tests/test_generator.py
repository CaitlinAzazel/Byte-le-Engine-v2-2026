
from typing import Sequence
import unittest

from game.common.game_object import GameObject
from game.common.items.item import Item
from game.common.avatar import Avatar
from game.common.player import Player
from game.common.map.game_board import GameBoard
from game.controllers.interact_controller import InteractController
from game.fnaacm.items.scrap import Scrap
from game.fnaacm.map.door import Door
from game.utils.vector import Vector
from game.common.enums import ActionType
from game.fnaacm.stations.generator import Generator

class TestGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.initial_scrap = 10
        generator_position = Vector()
        self.avatar = Avatar(position=generator_position, max_inventory_size=self.initial_scrap)
        self.scrap = Scrap(quantity=self.initial_scrap)
        self.inventory: list[Item] = [self.scrap, ]
        self.avatar.inventory = self.inventory

        self.player = Player(avatar=self.avatar)

        self.doors = [Door(), Door()]
        self.cost: int = 3
        self.generator = Generator(cost=self.cost, doors=self.doors)
        locations = { 
            generator_position: [self.generator, ], 
            Vector(1,1): self.doors,
        }
        self.game_board = GameBoard(None, Vector(4, 4), locations, False)
        self.game_board.generate_map()
        self.interact_controller = InteractController()

    # can the avatar interact with the generator? does the generator take their scrap?
    def test_handle_action(self):
        self.assertGreater(self.initial_scrap, self.cost)
        self.interact_controller.handle_actions(ActionType.INTERACT_CENTER, self.player, self.game_board)
        self.assertEqual(self.scrap.quantity, self.initial_scrap - self.cost)

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

    def test_to_and_from_json(self):
        data: dict = self.generator.to_json()
        generator: Generator = Generator().from_json(data)
        self.assertEqual(self.generator.object_type, generator.object_type)
        self.assertEqual(self.generator.cost, generator.cost)

    def test_doors_open_on_activated(self):
        self.test_activates_on_interact()
        for door in self.doors:
            self.assertTrue(door.open)

    def test_doors_stay_closed_on_failed_interact(self):
        self.test_not_enough_scrap()
        for door in self.doors:
            self.assertFalse(door.open)

