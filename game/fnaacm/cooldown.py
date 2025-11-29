from typing import Self, override
from warnings import deprecated
from game.common.game_object import GameObject
from game.fnaacm.timer import Timer

@deprecated(f'use Timer instead')
class Cooldown(GameObject):
    def __init__(self, duration: int = 1):
        """
        a Timer that always forces reset

        if a cooldown is activated on turn n,
        the next turn it may be activated is turn n + duration
        """
        super().__init__()
        if duration < 1:
            raise ValueError(f'cooldown duration must be nonpositive; value was {duration}')
        self.__timer = Timer(duration)

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, Cooldown) and \
            self.__timer == value.__timer

    @override
    def to_json(self) -> dict:
        data = super().to_json()
        data['timer'] = self.__timer.to_json()
        return data

    @override
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.__timer = Timer().from_json(data['timer'])
        return self

    @property
    def can_activate(self) -> bool:
        return self.__timer.done

    @property
    def turns_left(self) -> int:
        return self.__timer.turns_left

    @property
    def duration(self) -> int:
        return self.__timer.duration

    def tick(self):
        self.__timer.tick()

    def activate(self) -> bool:
        """
        returns True if successfully activated
        """
        return self.__timer.reset(force=False)

