import unittest
import pytest

from game.utils.vector import Vector
import game.test_suite.utils

class TestVector(unittest.TestCase):
    """
    `Test Vector Notes:`

        This class tests the different methods in the Vector class.
    """

    def setUp(self) -> None:
        self.vector1: Vector = Vector(8, 10)
        self.vector2: Vector = Vector(x=5, y=5)
        self.utils = game.test_suite.utils

    # test sets
    def test_vector_set_x(self) -> None:
        self.vector1.x = 5
        self.assertEqual(self.vector1.x, 5)

    def test_vector_set_x_fail(self) -> None:
        with self.assertRaises(ValueError) as e:
            self.vector1.x = 'test'
        self.assertTrue(self.utils.spell_check(str(e.exception), f'The given x value, {"test"}, is not an integer.', False))

    def test_vector_set_y(self) -> None:
        self.vector1.y = 5
        self.assertEqual(self.vector1.y, 5)

    def test_vector_set_y_fail(self) -> None:
        with self.assertRaises(ValueError) as e:
            self.vector1.y = 'test'
        self.assertTrue(self.utils.spell_check(str(e.exception), f'The given y value, {"test"}, is not an integer.', False))

    def test_vector_from_xy_tuple(self) -> None:
        self.assertEqual(Vector.from_xy_tuple((8, 10)), self.vector1)

    def test_vector_from_yx_tuple(self) -> None:
        self.assertEqual(Vector.from_yx_tuple((10, 8)), self.vector1)

    def test_vector_add_vectors(self) -> None:
        self.assertEqual(Vector.add_vectors(self.vector1, self.vector2), Vector(13, 15))

    def test_vector_add_to_vector(self) -> None:
        self.assertEqual(self.vector1.add_to_vector(self.vector2), Vector(13, 15))

    def test_vector_add_x_y(self) -> None:
        self.assertEqual(self.vector1.add_x_y(5, 5), Vector(13, 15))

    def test_vector_add_x(self) -> None:
        self.assertEqual(self.vector1.add_x(5), Vector(13, 10))

    def test_vector_add_y(self) -> None:
        self.assertEqual(self.vector1.add_y(5), Vector(8, 15))

    def test_vector_as_tuple(self) -> None:
        self.assertEqual(self.vector1.as_tuple(), (8, 10))

    def test_vector_json(self) -> None:
        data: dict = self.vector1.to_json()
        new_vector: Vector = Vector().from_json(data=data)
        self.assertEqual(self.vector1.object_type, new_vector.object_type)
        self.assertEqual(self.vector1.x, new_vector.x)
        self.assertEqual(self.vector1.y, new_vector.y)

    def test_vector_str(self) -> None:
        self.assertEqual(str(self.vector1), 'Coordinates: (8, 10)')

    def test_vector_add(self) -> None:
        self.assertEqual(self.vector1 + self.vector2, Vector(13, 15))

    def test_vector_sub(self) -> None:
        self.assertEqual(self.vector1 - self.vector2, Vector(3, 5))

    def test_vector_mul(self) -> None:
        self.assertEqual(self.vector1 * self.vector2, Vector(40, 50))

    def test_vector_scalar_mul(self) -> None:
        self.assertEqual(self.vector2 * 10, Vector(self.vector2.x * 10, self.vector2.y * 10))

    def test_vector_scalar_rmul(self) -> None:
        scalar = 9
        self.assertEqual(scalar * self.vector2, self.vector2 * scalar)

    def test_vector_floordiv(self) -> None:
        self.assertEqual(self.vector1 // Vector(0, 0), None)
        self.assertEqual(self.vector1 // self.vector2, Vector(1, 2))

    def test_vector_neg(self) -> None:
        self.assertEqual(self.vector1 != self.vector2, True)
        self.assertEqual(self.vector1 != Vector(8, 10), False)

    def test_vector_eq(self) -> None:
        self.assertEqual(self.vector1 == self.vector2, False)
        self.assertEqual(self.vector1 == Vector(8, 10), True)

    def test_vector_lt(self) -> None:
        self.assertEqual(self.vector1 < self.vector2, False)
        self.assertEqual(self.vector1 < Vector(8, 11), False)
        self.assertEqual(self.vector1 < Vector(9, 11), True)

    def test_vector_gt(self) -> None:
        self.assertEqual(self.vector1 > self.vector2, True)
        self.assertEqual(self.vector1 > Vector(8, 9), False)

    def test_vector_le(self) -> None:
        self.assertEqual(self.vector1 <= self.vector2, False)
        self.assertEqual(self.vector1 <= Vector(10, 11), True)
        self.assertEqual(self.vector1 <= Vector(8, 10), True)

    def test_vector_ge(self) -> None:
        self.assertEqual(self.vector1 >= self.vector2, True)
        self.assertEqual(self.vector1 >= Vector(8, 10), True)

    def test_vector_hash(self) -> None:
        self.assertEqual(hash(self.vector1), hash(self.vector1.as_tuple()))

    def test_vector_length(self) -> None:
        self.assertEqual(self.vector1.length(), 18)

    def test_vector_negative(self) -> None:
        self.assertEqual(self.vector1.negative(), Vector(-8, -10))

    def test_vector_distance(self) -> None:
        self.assertEqual(self.vector1.distance(self.vector2), 8)

    def test_farther_from(self) -> None:
        self.assertTrue(Vector(6, 7).is_farther_from(Vector(0, 0), Vector(1, 1)))

    def test_closer_to(self) -> None:
        self.assertTrue(Vector(6, 7).is_closer_to(Vector(0, 0), Vector(100, 0)))

    def test_equally_far(self) -> None:
        self.assertFalse(Vector(198, 198).is_farther_from(Vector(99, 99), Vector(0, 0)))
    # yes this is redundant
    def test_equally_close(self) -> None:
        self.assertFalse(Vector(-1, 0).is_closer_to(Vector(0, 1), Vector(1, 0)))

    # TODO: test edge cases like
    # WP
    # BW
    # W = wall
    # P = player
    # B = bot
    def test_overlapped_pos_correct_tiles(self):
        actual_positions = Vector.get_positions_overlapped_by_line(Vector(0, 0), Vector(1, 2))
        expected_positions = [
            Vector(0, 0),
            Vector(0, 1),
            Vector(1, 1),
            Vector(1, 2)
        ]
        for position in actual_positions:
            self.assertIn(position, expected_positions, f'did not find {position} in expected')
            print(f'{position.x} {position.y}')
        for position in expected_positions:
            self.assertIn(position, actual_positions, f'did not find {position} in actual')

    def test_overlapped_pos_returned_in_order(self):
        line_start = Vector(0, 0)
        positions = Vector.get_positions_overlapped_by_line_sorted_by_distance(line_start, Vector(6, 7))
        previous_position = positions[0]
        for position in positions[1:]:
            self.assertTrue(position.is_farther_from(line_start, previous_position), f'{position} is closer to {line_start} than {previous_position}')
            previous_position = position

    def test_overlapped_pos_upwards(self):
        actual_positions = Vector.get_positions_overlapped_by_line(Vector(0, 2), Vector(0, 0))
        expected_positions = [
            Vector(0, 2),
            Vector(0, 1),
            Vector(0, 0),
        ]
        self.assertListEqual(actual_positions, expected_positions)

    def test_direction_to(self):
        self.assertEqual(Vector(0, 0).direction_to(Vector(1, 1)), Vector(1, 1))
        self.assertEqual(Vector(0, 0).direction_to(Vector(5, 5)), Vector(1, 1))
        self.assertEqual(Vector(0, 0).direction_to(Vector(1000, 7)), Vector(1, 1))
        self.assertEqual(Vector(0, 0).direction_to(Vector(1, 0)), Vector(1, 0))
        self.assertEqual(Vector(0, 0).direction_to(Vector(10, 0)), Vector(1, 0))
        self.assertEqual(Vector(0, 0).direction_to(Vector(0, -999)), Vector(0, -1))
        self.assertEqual(Vector(0, 0).direction_to(Vector(-6, -7)), Vector(-1, -1))

    def test_is_diagonal(self):
        self.assertTrue(Vector(1, 1).is_diagonal)
        self.assertTrue(Vector(-8, 1).is_diagonal)
        self.assertTrue(Vector(1, -8).is_diagonal)
        self.assertTrue(Vector(-8, -9).is_diagonal)

        self.assertFalse(Vector(0, 0).is_diagonal)
        self.assertFalse(Vector(1, 0).is_diagonal)
        self.assertFalse(Vector(-1, 0).is_diagonal)
        self.assertFalse(Vector(-999, 0).is_diagonal)
        self.assertFalse(Vector(0, 10).is_diagonal)
        self.assertFalse(Vector(0, -12309).is_diagonal)

    def test_read_only(self):
        vector = Vector(read_only=True)
        with pytest.raises(RuntimeError, match='read-only'):
            vector.x = 1
        with pytest.raises(RuntimeError, match='read-only'):
            vector.y = 1
