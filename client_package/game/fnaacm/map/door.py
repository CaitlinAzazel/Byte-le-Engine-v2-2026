from game.common.map.occupiable import Occupiable
from game.common.enums import ObjectType


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

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, Door) and \
            self.open == value.open

    @property
    def open(self) -> bool:
        ...

    @open.setter
    def open(self, value):
        if not isinstance(value, bool):
            raise ValueError('The value must be of type bool')
        self._open = value
