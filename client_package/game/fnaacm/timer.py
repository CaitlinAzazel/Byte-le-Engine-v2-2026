from typing import override
from game.common.game_object import GameObject


class Timer(GameObject):
    """
    tracks a countdown

    if a timer starts on tick X, it will be done on turn (X + duration)
    """

    def __init__(self, duration: int = 1):
        super().__init__()
        self.duration = duration
        self.__turns_left = 0

    @override
    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, Timer) and \
            self.__duration == value.__duration and \
            self.__turns_left == value.__turns_left

    @property
    def done(self) -> bool:
        """
        should be called after `tick()`
        """
        ...

    @property
    def duration(self) -> int:
        return self.__duration

    @property
    def turns_left(self) -> int:
        return self.__turns_left

    @duration.setter
    def duration(self, turns: int) -> None:
        if not isinstance(turns, int):
            raise TypeError(
                f'{self.__class__.__name__}.duration must be an int '
                f'(was a(n) {value.__class__.__name__})')
        if turns < 1:
            raise ValueError(f'{self.__class__.__name__}.duration must be nonpositive (was {turns})')
        self.__duration = turns

    def tick(self):
        ...

    def reset(self, duration: int = -1, force: bool = True) -> bool:
        """
        :param duration: uses `self.duration` by default
        :param force: if True, reset the timer without checking if it is `done`
        :return: if the timer was reset
        """
        ...

    def force_done(self) -> None:
        ...
