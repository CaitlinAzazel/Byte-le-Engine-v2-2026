from typing import Sequence
import unittest

from game.common.enums import ActionType
from game.common.items.item import Item
from game.common.avatar import Avatar
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.movement_controller import MovementController
from game.controllers.interact_controller import InteractController
from game.utils.vector import Vector
from game.fnaacm.items.scrap import Scrap
from game.fnaacm.map.door import Door
from game.fnaacm.stations.generator import Generator

"""
Since bots don't exist in this branch, we're only testing the Player functionality with the door class.

Can they walk through a door when it's closed/deactivated 
Can they walk through a door when it's open/activated

"""

class TestDoor(unittest.TestCase):
    def setUp(self) -> None:
        self.avatar = Avatar(Vector(0,1))
        self.player = Player(avatar = self.avatar)
        self.movement_controller = MovementController()
        self.door = Door()
        self.door_vector = Vector(1,1)

        locations = { self.avatar.position : [self.avatar], self.door_vector : [self.door] }

        self.game_board = GameBoard(None, Vector(3, 3), locations, False)
        self.game_board.generate_map()

    # Can a player walk through a door that is closed? (Default Door State)
    def test_closed_status(self):
        self.assertFalse(self.door.open)
        self.starting_position = self.avatar.position
        self.movement_controller.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.assertEqual(self.starting_position, self.avatar.position)