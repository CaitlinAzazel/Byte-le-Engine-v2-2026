from typing import Self, override
from game.common.game_object import GameObject

# TODO: testing 8^)

class Cooldown(GameObject):
    def __init__(self, duration: int = 0):
        """
        encapsulates simple turn-based cooldown logic; proper use requires that `tick` is called before checking `can_activate`
        """
        super().__init__()
        self.__duration = duration
        self.__counter = 0

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, self.__class__):
            return self.__dict__ == value.__dict__
        return False

    @override
    def to_json(self) -> dict:
        data = super().to_json()
        data['duration'] = self.__duration
        data['counter'] = self.__counter
        return data

    @override
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.__duration = data['duration']
        self.__counter = data['counter']
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

