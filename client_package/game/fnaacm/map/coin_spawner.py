from game.common.enums import ObjectType
from game.common.map.occupiable import Occupiable
from game.fnaacm.game_object_list import GameObjectList
from game.fnaacm.ldtk_entity import LDtkEntity
from game.fnaacm.timer import Timer
from game.utils.vector import Vector


class CoinSpawner(Occupiable, LDtkEntity):
    """
    A tile that occasionally holds coins which increase the player's points

    The player's avatar collects coins by walking over this tile when they are available
    """

    class LDtkFieldIdentifers:
        TURNS_TO_RESPAWN = 'turns_to_respawn'
        POINT_VALUE = 'point_value'

    def __init__(self, position: Vector = Vector(0,0), turns_to_respawn: int = 1, point_value: int = 1) -> None:
        super().__init__()
        self.object_type: ObjectType = ObjectType.COIN_SPAWNER
        self.position: Vector = position
        self.point_value: int = point_value
        self.__timer = Timer(duration=turns_to_respawn)

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, self.__class__):
            return \
                self.position == value.position and \
                self.__timer == value.__timer and \
                self.point_value == value.point_value
        return False

    @property
    def is_available(self) -> bool:
        ...

class CoinSpawnerList(GameObjectList[CoinSpawner]):
    def __init__(self):
        super().__init__('coins', CoinSpawner)
