import unittest
from game.controllers.bot_movement_controller import BotMovementController
from game.utils.vector import Vector
from game.common.map.game_board import GameBoard
from game.fnaacm.map.vent import Vent
from game.fnaacm.bots.ian_bot import IANBot
from game.common.avatar import Avatar
from game.common.player import Player
from game.common.enums import ActionType


class TestIANBot(unittest.TestCase):
    def setUp(self):
        # Create board and player
        self.board = GameBoard(map_size=Vector(5, 5))
        self.board.generate_map()
        self.player_avatar = Avatar(position=Vector(2, 2))
        self.player = Player(avatar=self.player_avatar)

        # Create bot at top-left
        self.bot = IANBot()
        self.bot.position = Vector(0, 0)

        self.bot_movement_controller = BotMovementController()

    def build_board(self, include_vent=False):
        # Reset board
        self.board = GameBoard(map_size=Vector(5, 5))
        self.board.generate_map()
        if include_vent:
            self.board.place(Vector(1, 0), Vent())
        return self.board

    def test_bot_respects_vent(self):
        board = self.build_board(include_vent=True)
        moves = self.bot_movement_controller.ian_hunt(self.bot, self.player_avatar, self.board)
        # IAN should never try to go through vent
        vent_pos = Vector(1, 0)
        for move in moves:
            new_pos = self.bot.position
            if move == ActionType.MOVE_UP:
                new_pos = Vector(new_pos.x, new_pos.y - 1)
            elif move == ActionType.MOVE_DOWN:
                new_pos = Vector(new_pos.x, new_pos.y + 1)
            elif move == ActionType.MOVE_LEFT:
                new_pos = Vector(new_pos.x - 1, new_pos.y)
            elif move == ActionType.MOVE_RIGHT:
                new_pos = Vector(new_pos.x + 1, new_pos.y)
            self.assertNotEqual(new_pos, vent_pos)

    def test_hunt_boosted_moves_every_turn(self):
        self.bot.boosted = True  # moves every turn
        board = self.build_board()
        moves = self.bot_movement_controller.ian_hunt(self.bot, self.player_avatar, self.board)
        self.assertEqual(len(moves), 2)

    def test_hunt_normal_moves_once(self):
        self.bot.boosted = False
        board = self.build_board()
        moves = self.bot_movement_controller.ian_hunt(self.bot, self.player_avatar, self.board)
        self.assertEqual(len(moves), 1)

    def test_hunt_move_toward_player(self):
        board = self.build_board()
        moves = self.bot_movement_controller.ian_hunt(self.bot, self.player_avatar, self.board)

        # Bot should have at least one move toward player
        self.assertTrue(len(moves) >= 1)

        # Map ActionType to vector change
        ACTION_TO_VECTOR = {
            ActionType.MOVE_UP: Vector(0, -1),
            ActionType.MOVE_DOWN: Vector(0, 1),
            ActionType.MOVE_LEFT: Vector(-1, 0),
            ActionType.MOVE_RIGHT: Vector(1, 0),
        }

        move_action = moves[0]
        if move_action in ACTION_TO_VECTOR:
            move_vector = ACTION_TO_VECTOR[move_action]
            start_distance = abs(self.bot.position.x - self.player_avatar.position.x) + \
                             abs(self.bot.position.y - self.player_avatar.position.y)
            next_distance = abs(self.bot.position.x + move_vector.x - self.player_avatar.position.x) + \
                            abs(self.bot.position.y + move_vector.y - self.player_avatar.position.y)
            self.assertLess(next_distance, start_distance)
        else:
            self.skipTest(f"{move_action} does not change position")

    def test_hunt_no_move_if_on_player(self):
        # Bot on same tile as player should not move
        self.bot.position = Vector(self.player_avatar.position.x, self.player_avatar.position.y)
        board = self.build_board()
        moves = self.bot_movement_controller.ian_hunt(self.bot, self.player_avatar, board)
        self.assertEqual(len(moves), 0)

    def test_patrol_returns_empty(self):
        # Patrol does not use the player
        moves = self.bot_movement_controller.ian_patrol()
        self.assertIsInstance(moves, list)
        self.assertEqual(len(moves), 0)


if __name__ == "__main__":
    unittest.main()
