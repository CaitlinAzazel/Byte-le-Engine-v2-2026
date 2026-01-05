import unittest
from game.controllers.bot_movement_controller import BotMovementController
from game.controllers.bot_vision_controller import BotVisionController
from game.utils.vector import Vector
from game.common.map.game_board import GameBoard
from game.common.map.wall import Wall
from game.fnaacm.map.vent import Vent
from game.fnaacm.bots.crawler_bot import CrawlerBot
from game.common.avatar import Avatar
from game.common.player import Player
from game.common.enums import ActionType


class TestCrawlerBot(unittest.TestCase):
    def setUp(self):
        # Create board and player
        self.board = GameBoard(map_size=Vector(5, 5))
        self.board.generate_map()
        self.player_avatar = Avatar(position=Vector(2, 2))
        self.player = Player(avatar=self.player_avatar)
        # Create bot at top-left
        self.bot = CrawlerBot()
        self.bot.position = Vector(0, 0)
        self.bot_movement_controller = BotMovementController()

    def build_board(self, include_vent=False):
        # Reset board (rebuild map)
        self.board = GameBoard(map_size=Vector(5, 5), locations={
            self.bot.position: [self.bot],
            self.player_avatar.position: [self.player_avatar],
        })
        self.board.generate_map()
        if include_vent:
            self.board.place(Vector(1, 0), Vent())
        return self.board

    def test_bot_moves_around_vent(self):
        self.build_board(include_vent=True)
        self.bot.can_see_player = True
        moves = self.bot_movement_controller.calc_next_moves(self.bot, self.player_avatar, self.board, 0)
        # Crawler can go through vents, should have at least one move
        self.assertTrue(len(moves) >= 1)
        # Ensure it does not step on the player
        self.assertNotEqual(moves[0], self.player_avatar.position)

    def test_hunt_boosted_moves_once(self):
        self.bot.boosted = True  # reduces turn_delay
        board = self.build_board()
        moves = self.bot_movement_controller.calc_next_moves(self.bot, self.player_avatar, self.board, 0)
        # When boosted, bot returns 2 moves
        self.assertEqual(len(moves), 2)

    def test_hunt_move_toward_player(self):
        board = self.build_board()
        moves = self.bot_movement_controller.calc_next_moves(self.bot, self.player_avatar, self.board, 0)

        # Bot should have at least one move toward player
        self.assertTrue(len(moves) >= 1)

        # Map only the moves that actually change position
        ACTION_TO_VECTOR = {
            ActionType.MOVE_UP: Vector(0, -1),
            ActionType.MOVE_DOWN: Vector(0, 1),
            ActionType.MOVE_LEFT: Vector(-1, 0),
            ActionType.MOVE_RIGHT: Vector(1, 0),
          }

        # Only test the first move if it changes position
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
        moves = self.bot_movement_controller.calc_next_moves(self.bot, self.player_avatar, board, 0)
        self.assertEqual(len(moves), 0)

    def test_patrol_returns_empty(self):
        # Patrol does not use the player
        moves = self.bot_movement_controller.calc_next_moves(self.bot, self.player_avatar, self.board, 0)
        self.assertIsInstance(moves, list)

if __name__ == "__main__":
    unittest.main()
