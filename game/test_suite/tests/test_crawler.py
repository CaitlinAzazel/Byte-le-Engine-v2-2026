import unittest
from game.common.enums import ObjectType
from game.utils.vector import Vector
from game.fnaacm.bots.crawler_bot import CrawlerBot  # Update with your actual import path
from game.common.avatar import Avatar
from game.common.map.game_object_container import GameObjectContainer
from game.common.map.wall import Wall
from game.common.game_object import GameObject


class DummyGameBoard:
    """
    Lightweight mock of the GameBoard for CrawlerBot unit tests.
    """

    def __init__(self):
        self.map_data = {}

    def is_valid_coords(self, coords: Vector) -> bool:
        return 0 <= coords.x < 5 and 0 <= coords.y < 5

    def is_occupiable(self, coords: Vector) -> bool:
        return self.is_valid_coords(coords) and not isinstance(self.get_top(coords), Wall)

    def place(self, coords: Vector, obj: GameObject) -> bool:
        self.map_data[coords] = GameObjectContainer([obj])
        return True

    def remove(self, coords: Vector, obj_type: ObjectType) -> GameObject | None:
        if coords in self.map_data and self.map_data[coords].get_top().object_type == obj_type:
            return self.map_data.pop(coords).get_top()
        return None

    def get_top(self, coords: Vector) -> GameObject | None:
        return self.map_data.get(coords).get_top() if coords in self.map_data else None


class TestCrawlerBot(unittest.TestCase):
    """
    `Test CrawlerBot Notes:`

        Tests that the crawler bot behaves correctly — moves every 4 turns, uses A* pathfinding,
        avoids unoccupiable tiles (like walls), and updates its position appropriately.
    """

    def setUp(self) -> None:
        self.bot = CrawlerBot()
        self.player = Avatar()
        self.board = DummyGameBoard()

        # Set initial positions
        self.bot.position = Vector(0, 0)
        self.player.position = Vector(2, 0)

        # Place both on the board
        self.board.place(self.bot.position, self.bot)
        self.board.place(self.player.position, self.player)

    def test_bot_moves_every_4_turns(self):
        for i in range(3):
            self.bot.take_turn(self.board, self.player)
            self.assertEqual(str(self.bot.position), str(Vector(0, 0)))  # No movement

        self.bot.take_turn(self.board, self.player)
        self.assertEqual(str(self.bot.position), str(Vector(1, 0)))  # Moves one step toward player

    def test_bot_pathfinding_to_player(self):
        # Move bot far from player
        self.bot.position = Vector(0, 0)
        self.player.position = Vector(3, 0)
        self.board.place(self.bot.position, self.bot)
        self.board.place(self.player.position, self.player)

        for _ in range(8):
            self.bot.take_turn(self.board, self.player)

        self.assertEqual(str(self.bot.position), str(Vector(2, 0)))  # Should be close to player (1 step away)

    def test_bot_does_not_move_into_wall(self):
        # Add wall in the way
        wall_position = Vector(1, 0)
        self.board.map_data[wall_position] = GameObjectContainer([Wall()])
        self.bot.take_turn(self.board, self.player)
        self.bot.take_turn(self.board, self.player)
        self.bot.take_turn(self.board, self.player)
        self.bot.take_turn(self.board, self.player)

        # Confirm the bot didn’t move into the wall
        self.assertEqual(str(self.bot.position), str(Vector(0, 0)))


if __name__ == '__main__':
    unittest.main()
