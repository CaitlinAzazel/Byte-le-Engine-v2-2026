from typing_extensions import override
from game.common.avatar import Avatar
from game.common.game_object import GameObject
from game.common.map.occupiable import Occupiable
from game.common.enums import ObjectType
from typing import Self, Type

class Door(Occupiable):
    """
        `Door Class Notes:`

            This file defines the class Door, which are game map tiles that can only be passed on certain conditions

            FNAACM uses doors that only open when requisite interactions are made with the 'Generator' class object

            These objects can only be occupied by GameObjects, so inheritance is important. The ``None`` value is
            acceptable for this too, showing that nothing is occupying the object.
        """

    def __init__(self):
        super().__init__()
        self.object_type: ObjectType = ObjectType.DOOR
        self._open = False

    @override
    def to_json(self) -> dict:
        json = super().to_json()
        json['open'] = self.open
        return json

    @override
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.open = data['open']
        return self

    @property
    def open(self) -> bool:
        return self._open

    @override
    def can_occupy(self, avatar: Avatar) -> bool:
        return self.open

    @open.setter
    def open(self, value):
        if not isinstance(value, bool):
            raise ValueError('The value must be of type bool')
        self._open = value