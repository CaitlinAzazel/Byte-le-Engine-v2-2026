from math import sqrt
from game.common.game_object import GameObject
from game.common.enums import ActionType, ObjectType
from typing import Self, Tuple, Union, overload


class Vector(GameObject):
    """
    `Vector Class Notes:`

    This class is used universally in the project to handle anything related to coordinates. There are a few useful
    methods here to help in a few situations.

    -----

    Add Vectors Method:
        This method will take two Vector objects, combine their (x, y) coordinates, and return a new Vector object.

        Example:
            vector_1: (1, 1)
            vector_2: (1, 1)

            Result:
            vector_result: (2, 2)

    -----

    Add to Vector method:
        This method will take a different Vector object and add it to the current Self reference; that is, this method
        belongs to a Vector object and is not static.

        Example:
            self_vector: (0, 0)
            vector_1: (1, 3)

            Result:
            self_vector: (1, 3)

    -----

    Add X and Add Y methods:
        These methods act similarly to the ``add_vector()`` method, but instead of changing both the x and y, these
        methods change their respective variables.

        Add X Example:
            self_vector: (0, 0)
            vector_1: (1, 3)

            Result:
            self_vector: (1, 0)

        Add Y Example:
            self_vector: (0, 0)
            vector_1: (1, 3)

            Result:
            self_vector: (0, 3)

    -----

    As Tuple Method:
        This method returns a tuple of the Vector object in the form of (x, y). This is to help with storing it easily
        or accessing it in an immutable structure.
    """

    def __init__(self, x: int = 0, y: int = 0):
        super().__init__()
        self.object_type: ObjectType = ObjectType.VECTOR
        self.x = x
        self.y = y

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, x: int) -> None:
        if x is None or not isinstance(x, int):
            raise ValueError(f"The given x value, {x}, is not an integer.")
        self.__x = x

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, y: int) -> None:
        if y is None or not isinstance(y, int):
            raise ValueError(f"The given y value, {y}, is not an integer.")
        self.__y = y

    @property
    def magnitude(self) -> float:
        return sqrt(self.magnitude_squared)

    @property
    def magnitude_squared(self) -> int:
        return self.x**2 + self.y**2

    @staticmethod
    def from_xy_tuple(xy_tuple: Tuple[int, int]) -> 'Vector':
        return Vector(*xy_tuple)

    @staticmethod
    def from_yx_tuple(yx_tuple: Tuple[int, int]) -> 'Vector':
        return Vector(*yx_tuple[::-1])

    @staticmethod
    def add_vectors(vector_1: 'Vector', vector_2: 'Vector') -> 'Vector':
        new_x: int = vector_1.x + vector_2.x
        new_y: int = vector_1.y + vector_2.y
        return Vector(new_x, new_y)

    def is_farther_from(self, origin: Self, other: Self):
        """
        is `self` farther from `origin` than `other`? false if equally far
        """
        return (self - origin).magnitude_squared > (other - origin).magnitude_squared

    def is_closer_to(self, origin: Self, other: Self):
        """
        is `self` closer to `origin` than `other`? false if equally close
        """
        return (self - origin).magnitude_squared < (other - origin).magnitude_squared

    def add_to_vector(self, other_vector: Self) -> 'Vector':
        return Vector(
            self.x + other_vector.x,
            self.y + other_vector.y
        )

    def add_x_y(self, x: int, y: int) -> 'Vector':
        return self.add_to_vector(Vector(x, y))

    def add_x(self, x: int) -> 'Vector':
        return self.add_to_vector(Vector(x))

    def add_y(self, y: int) -> 'Vector':
        return self.add_to_vector(Vector(y=y))

    def as_tuple(self) -> Tuple[int, int]:
        """Returns (x: int, y: int)"""
        return self.x, self.y

    def to_json(self) -> dict:
        data = super().to_json()
        data['x'] = self.x
        data['y'] = self.y

        return data

    def from_json(self, data) -> Self:
        super().from_json(data)
        self.x = data['x']
        self.y = data['y']

        return self

    # Overloaded Methods
    def __str__(self) -> str:
        return f"Coordinates: ({self.x}, {self.y})"

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x - other.x, self.y - other.y)

    @overload
    def __mul__(self, other: int) -> 'Vector':
        ...
    @overload
    def __mul__(self, other: 'Vector') -> 'Vector':
        ...
    def __mul__(self, other) -> 'Vector':
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)
        else:
            return Vector(self.x * other, self.y * other)

    def __rmul__(self, scalar: int) -> 'Vector':
        return self * scalar

    def __floordiv__(self, other: 'Vector') -> Union['Vector', None]:
        if other.x == 0 or other.y == 0:
            return None
        return Vector(self.x // other.x, self.y // other.y)

    def __ne__(self, other: 'Vector') -> bool:
        return hash(str(self)) != hash(str(other))

    def __eq__(self, other: 'Vector') -> bool:
        return hash(str(self)) == hash(str(other))

    def __lt__(self, other: 'Vector') -> bool:
        return self.x < other.x and self.y < other.y

    def __gt__(self, other: 'Vector') -> bool:
        return self.x > other.x and self.y > other.y

    def __le__(self, other: 'Vector') -> bool:
        return self.x <= other.x and self.y <= other.y

    def __ge__(self, other: 'Vector') -> bool:
        return self.x >= other.x and self.y >= other.y

    def __hash__(self) -> int:
        return hash(self.as_tuple())

    def length(self) -> int:
        return abs(self.x) + abs(self.y)

    def negative(self) -> Self:
        return Vector(-self.x, -self.y)

    def distance(self, other_vector: 'Vector') -> int:
        return abs(self.x - other_vector.x) + abs(self.y - other_vector.y)
