import unittest

from game.common.enums import ActionType
from game.common.stations.refuge import Refuge
from game.common.player import Player
from game.common.game_object import GameObject
from game.common.avatar import Avatar
from game.common.map.game_board import GameBoard
from game.controllers.bot_movement_controller import BotMovementController
from game.controllers.movement_controller import MovementController
from game.utils.vector import Vector
from game.fnaacm.bots.dumb_bot import DumbBot
from game.fnaacm.map.vent import Vent
from game.common.map.wall import Wall


class TestDumbBot(unittest.TestCase):
    def setUp(self):
        self.locations: dict[Vector, list[GameObject]] = {}
        self.game_board = GameBoard(None, Vector(3, 3), self.locations, False)
        self.game_board.generate_map()
        self.bot = DumbBot()
        self.refuge = Refuge(1,1)
        self.avatar = Avatar()
        self.vent = Vent()
        self.wall = Wall()
        self.actions: list[ActionType] = []
        self.player = Player(None, None, self.actions, self.avatar)
        self.movement_controller = BotMovementController()




    def test_can_see_player(self):
        self.game_board.place(Vector(0,0), self.bot)
        self.game_board.place(Vector(1,1),self.avatar)

        self.assertTrue(self.bot.can_see_player(self.game_board, self.player))

    def test_movement_seen_unstunned(self):
        self.game_board.place(Vector(0,0), self.bot)
        self.game_board.place(Vector(1,1),self.avatar)
        ## Check if you actually initialize tuff

        print(self.bot.can_see_player(self.game_board, self.player))
        movement = self.bot.calc_next_move(self.game_board, self.player)
        print(movement[0])
        self.movement_controller.handle_actions(movement[0], self.bot, self.game_board)
        print(self.bot.position)
        self.assertTrue(self.bot.position == (Vector(1,0)))

    def test_movement_seen_stunned(self):
        locations_open: dict[Vector, list[GameObject]] = {
            Vector(0, 0): [self.bot],
            Vector(1, 1): [self.avatar]
        }
        game_board = GameBoard(None, Vector(3,3), locations_open, True)
        game_board.generate_map()

        self.bot.stunned = True
        self.assertTrue(self.bot.can_see_player(game_board, self.player))

    def test_movement_unseen_stunned(self):
        locations_walled: dict[Vector, list[GameObject]] = {
            Vector(0, 1): [self.wall],
            Vector(1, 1): [self.wall],
            Vector(2, 1): [self.wall],
            Vector(3, 1): [self.wall],
            Vector(0, 0): [self.bot],
            Vector(1, 2): [self.avatar],
            }
        game_board = GameBoard(None, Vector(3,3), locations_walled, True)
        game_board.generate_map()

        self.bot.stunned = True
        self.assertFalse(self.bot.can_see_player(game_board, self.player))


    def test_movement_unseen_refuge(self):
        locations_refuge: dict[Vector, list[GameObject]] = {
            Vector(1, 1): [self.refuge],
            Vector(0, 0): [self.bot],
            Vector(1, 1): [self.avatar]
        }
        game_board = GameBoard(None, Vector(3, 3), locations_refuge, True)
        game_board.generate_map()

        movement = self.bot.calc_next_move(self.game_board, self.player)
        print(movement[0])
        self.movement_controller.handle_actions(movement[0], self.bot, self.game_board)
        print(self.bot.position)
        self.assertFalse(self.bot.can_see_player(game_board, self.player))

    def test_movement_unseen_vent(self):
        locations_vent: dict[Vector, list[GameObject]] = {
            Vector(1, 1): [self.vent],
            Vector(0, 0): [self.bot],
            Vector(1, 1): [self.avatar],
        }
        game_board = GameBoard(None, Vector(3, 3), locations_vent, True)
        game_board.generate_map()

        self.assertFalse(self.bot.can_see_player(game_board, self.player))


    def test_movement_unseen_wall(self):
        locations_walled: dict[Vector, list[GameObject]] = {
            Vector(0, 1): [self.wall],
            Vector(1, 1): [self.wall],
            Vector(2, 1): [self.wall],
            Vector(3, 1): [self.wall],
            Vector(0, 0): [self.bot],
            Vector(1, 2): [self.avatar],
        }
        game_board = GameBoard(None, Vector(3, 3), locations_walled, True)
        game_board.generate_map()

        self.assertFalse(self.bot.can_see_player(game_board, self.player))



    def test_vision_boosted(self):
        locations_open: dict[Vector, list[GameObject]] = {
            Vector(2, 2): [self.bot],
            Vector(0, 0): [self.avatar]
        }
        game_board = GameBoard(None, Vector(3, 3), locations_open, False)
        game_board.generate_map()
        self.bot.boosting(True)
        print(self.bot.boosted)

        self.assertTrue(self.bot.can_see_player(game_board, self.player))




        """
            -- Test Movement Seen - Stunned
            -- Test Movement Seen - Unstunned
            -- Test Movement Unseen - Stunned
            -- Test Movement Unseen - Unstunned - Refuge
            -- Test Movement Unseen - Unstunned - Vent
            -- Test Movement Unseen - Unstunned - Wall
            -- Test Vision Boosted
        """
