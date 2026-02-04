from game.common.enums import ObjectType
from game.common.map.occupiable import Occupiable
from game.fnaacm.ldtk_entity import LDtkEntity
from game.fnaacm.timer import Timer
from game.utils.vector import Vector

class ScrapSpawner(Occupiable, LDtkEntity):
    """
    A tile that occasionally holds scrap (generator fuel).
    """


    def __init__(self, position: Vector = Vector(0, 0), turns_to_respawn: int = 1, point_value: int = 1) -> None:
        super().__init__()
        self.object_type: ObjectType = ObjectType.SCRAP_SPAWNER
        self.position: Vector = position
        self.point_value: int = point_value
        self.__timer: Timer = Timer(turns_to_respawn)

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, self.__class__) and \
            self.position == value.position and \
            self.__timer == value.__timer and \
            self.point_value == value.point_value

    @property
    def is_available(self) -> bool:
        ...

