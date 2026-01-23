import json
from math import floor, sqrt
from game.common.game_object import GameObject
from game.common.enums import ActionType, ObjectType
from typing import Self, Tuple, Union, overload

from game.utils.helpers import clamp


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

    @staticmethod
    def dict_from_json_str(json_str: str) -> dict:
        # our jsons use single quotes for some reason
        return json.loads(json_str.replace('\'', '\"'))

    @classmethod
    def from_json_str(cls, json_str: str) -> Self:
        data = Vector.dict_from_json_str(json_str)
        return cls(data['x'], data['y'])

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

    def clamp_xy(self, min: int, max: int) -> Self:
        self.clamp_x(min, max)
        self.clamp_y(min, max)
        return self

    def clamp_x(self, min: int, max: int) -> Self:
        self.x = clamp(self.x, min, max)
        return self

    def clamp_y(self, min: int, max: int) -> Self:
        self.y = clamp(self.y, min, max)
        return self

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

    @staticmethod
    def _get_progress(a: float, b: float, value: float) -> float:
        """
        returns percentage "progress" of value from a to b
        if value is "past" b then progress is 100%
        """
        # you cannot move "between" a and b if a == b
        if a == b:
            return 1
        return abs((value - a) / (b - a))

    # https://forum.gamemaker.io/index.php?threads/how-to-find-every-square-a-line-passes-through.101130/
    @staticmethod
    def get_positions_overlapped_by_line(line_start: 'Vector', line_end: 'Vector') -> list['Vector']:
        overlapped_positions = []
        # // get grid-relative coordinates
        # var cx1 = x1 / cell_size;
        # var cy1 = y1 / cell_size;
        # var cx2 = x2 / cell_size;
        # var cy2 = y2 / cell_size;
        cx1 = line_start.x + 0.5
        cy1 = line_start.y + 0.5
        cx2 = line_end.x + 0.5
        cy2 = line_end.y + 0.5

        # // setup the initial parameters
        # var xdir = x2 > x1 ? 1 : -1;
        xdir: int = 1 if cx2 > cx1 else -1
        # var xcurrent = floor(cx1);
        xcurrent: int = floor(cx1)
        # var xnext = x2 > x1 ? xcurrent + 1 : xcurrent;
        xnext: float = (xcurrent + 1) if cx2 > cx1 else (xcurrent)
        # var xprogress = get_progress(cx1, cx2, xnext);
        xprogress = Vector._get_progress(cx1, cx2, xnext)

        # var ydir = y2 > y1 ? 1 : -1;
        ydir = 1 if cy2 > cy1 else -1
        # var ycurrent = floor(cy1);
        ycurrent = floor(cy1)
        # var ynext = y2 > y1 ? ycurrent + 1 : ycurrent;
        ynext = (ycurrent + 1) if cy2 > cy1 else (ycurrent)
        # var yprogress = get_progress(cy1, cy2, ynext);
        yprogress = Vector._get_progress(cy1, cy2, ynext)
        #
        # // if at this point x progress or y progress is 0
        # // then the starting point is somewhere at a grid boundary
        # // and the first cell to draw will be determined by the crawl
        #
        # // if neither progress is 0, the starting point is in the middle of a cell
        # // and thus a cell containing the point should be drawn before the crawl
        # if (xprogress != 0 && yprogress != 0)
        #     draw_cell(xcurrent, ycurrent);
        if (xprogress != 0 and yprogress != 0):
            overlapped_positions.append(Vector(xcurrent, ycurrent))
        #
        # // the line-crawl loop
        #
        # // if the upcoming x progress is lower than the y progress
        # // then it means the upcoming horizontal intersection between lines is closer
        # // and thus the line should crawl horizontally in the next step
        #
        # // conversely, if the y progress is larger than the x progress
        # // the line should crawl vertically in the next step
        #
        # // if x progress and y progress are the same
        # // the line crawls diagonally, skipping both nearby cells
        # while (xprogress < 1 || yprogress < 1) {
        while (xprogress < 1 or yprogress < 1):
            # var should_move_x = xprogress <= yprogress;
            # var should_move_y = yprogress <= xprogress;
            should_move_x = xprogress <= yprogress
            should_move_y = yprogress <= xprogress

            # if (should_move_x) {
            # xcurrent += xdir;
            # xnext += xdir;
            # xprogress = get_progress(cx1, cx2, xnext);
            # }
            if should_move_x:
                xcurrent += xdir
                xnext += xdir
                xprogress = Vector._get_progress(cx1, cx2, xnext)

            # if (should_move_y) {
            # ycurrent += ydir;
            # ynext += ydir;
            # yprogress = get_progress(cy1, cy2, ynext);
            # }
            if should_move_y:
                ycurrent += ydir
                ynext += ydir
                yprogress = Vector._get_progress(cy1, cy2, ynext)

            overlapped_positions.append(Vector(xcurrent, ycurrent))
        # }

        return overlapped_positions

    @staticmethod
    def get_positions_overlapped_by_line_sorted_by_distance(line_start: 'Vector', line_end: 'Vector') -> list['Vector']:
        # lowkey made this for no reason
        return sorted(Vector.get_positions_overlapped_by_line(line_start, line_end),
                      key=lambda pos: (pos - line_start).magnitude_squared)

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
