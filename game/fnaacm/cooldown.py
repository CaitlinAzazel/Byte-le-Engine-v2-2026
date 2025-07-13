from typing import Self, override
from game.common.game_object import GameObject

DURATION_JSON_KEY = 'duration'
COUNTER_JSON_KEY = 'counter'

# TODO: testing 8^)

class Cooldown(GameObject):
    def __init__(self, duration: int = 0):
        """
        encapsulates simple turn-based cooldown logic; proper use requires that `tick` is called before checking `can_activate`
        """
        super().__init__()
        self.__duration = duration
        self.__counter = 0

    @override
    def to_json(self) -> dict:
        data = super().to_json()
        data[DURATION_JSON_KEY] = self.__duration
        data[COUNTER_JSON_KEY] = self.__counter
        return data

    @override
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.__duration = data[DURATION_JSON_KEY]
        self.__counter = data[COUNTER_JSON_KEY]
        return self

    def tick(self):
        """
        should be called BEFORE checking `can_activate`
        """
        if self.__counter <= 0:
            return
        self.__counter -= 1

    @property
    def can_activate(self) -> bool:
        """
        returns True if cooldown was successfully activated
        """
        return self.__counter == 0

    def activate(self) -> bool:
        if not self.can_activate:
            return False
        self.__counter = self.__duration
        return True

