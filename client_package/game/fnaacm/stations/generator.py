from game.common.enums import ObjectType
from game.common.items.item import Item
from game.common.stations.station import Station
from game.fnaacm.ldtk_entity import LDtkEntity
from game.fnaacm.map.door import Door


class Generator(Station, LDtkEntity):
    """
    Opens connected doors once fed scrap via interaction.
    Can also be forcibly disabled (e.g., from attacks).
    """

    def __init__(self, held_item: Item | None = None, cost: int = 1, doors: list[Door] = [], point_bonus: int = 0):
        super().__init__(held_item=held_item)
        self.object_type: ObjectType = ObjectType.GENERATOR
        self.connected_doors: list[Door] = doors
        self.__active: bool = False
        self.__cost: int = cost
        self.__point_bonus: int = point_bonus
        self.__is_bonus_collected: bool = False

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, Generator) and \
            self.connected_doors == value.connected_doors and \
            self.active == value.active and \
            self.cost == value.cost and \
            self.passive_point_bonus == value.passive_point_bonus

    @property
    def active(self) -> bool:
        return self.__active

    @property
    def cost(self) -> int:
        return self.__cost

    @cost.setter
    def cost(self, value: object):
        if not isinstance(value, int):
            raise TypeError(f'{self.__class__}.cost must be an int; {value} is a(n) {value.__class__}')
        self.__cost = value

    @property
    def passive_point_bonus(self) -> int:
        ...

    @property
    def activation_point_bonus(self) -> int:
        ...

    @property
    def is_bonus_collected(self) -> bool:
        ...

