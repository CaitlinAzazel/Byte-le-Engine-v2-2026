import unittest

from game.common.avatar import Avatar
from game.common.items.item import Item
from game.controllers.interact_controller import InteractController
from game.common.map.game_board import GameBoard
from game.utils.vector import Vector
from game.common.map.wall import Wall
from game.common.stations.station import Station
from game.common.stations.station_example import StationExample
from game.common.stations.station_receiver_example import StationReceiverExample
from game.common.stations.occupiable_station import OccupiableStation
from game.common.stations.occupiable_station_example import OccupiableStationExample
from game.common.game_object import GameObject
from game.common.action import ActionType
from game.common.player import Player
from game.common.enums import ObjectType


class TestInteractController(unittest.TestCase):
    """
    `Test Avatar Notes:`

        This class tests the different methods in the InteractController class.
    """

    def setUp(self) -> None:
        self.interact_controller: InteractController = InteractController()
        self.avatar: Avatar = Avatar(Vector(4, 5))
        self.locations: dict[Vector, list[GameObject]] = {
            Vector(1, 1): [Station(None)],
            Vector(5, 4): [self.occupiable_station(None)],
            Vector(6, 5): [self.station(None)],
            Vector(4, 5): [self.avatar],
            Vector(5, 5): [self.bot],
        }
        self.game_board: GameBoard = GameBoard(1, Vector(10, 10), self.locations, False)
        self.player: Player = Player(None, None, [], self.avatar)
        self.game_board.generate_map()

    # attack and attack nothing
    def test_attack_nothing(self):
        self.interact_controller.handle_actions(ActionType.ATTACK_DOWN, self.bot, self.game_board)
        self.assertEqual(self.bot.attack, None)


    # interact and pick up from a station
    def test_attack_player_station(self):
        self.interact_controller.handle_actions(ActionType.ATTACK_LEFT, self.player, self.game_board)
        self.assertEqual(self.bot.attack, self.player)


