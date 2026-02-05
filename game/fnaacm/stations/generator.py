from typing import Self, override
from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.items.item import Item
from game.common.stations.station import Station
from game.fnaacm.items.scrap import Scrap
from game.fnaacm.ldtk_entity import LDtkEntity
from game.fnaacm.map.door import Door
from game.utils.ldtk_json import EntityInstance


class Generator(Station, LDtkEntity):
    """
    Opens connected doors once fed scrap via interaction.
    Can also be forcibly disabled (e.g., from attacks).
    """

    class LDtkFieldIdentifiers:
        COST = 'cost'
        CONNECTED_DOORS = 'connected_doors'
        ACTIVATION_BONUS = 'activation_bonus'
        MULTIPLIER_BONUS = 'multiplier_bonus'

    def __init__(self, held_item: Item | None = None, cost: int = 1, doors: list[Door] = [], activation_bonus: int = 0, multiplier_bonus: float = 0.0):
        super().__init__(held_item=held_item)
        self.object_type: ObjectType = ObjectType.GENERATOR
        self.connected_doors: list[Door] = doors
        self.__active: bool = False
        self.__cost: int = cost
        self.__activation_bonus: int = activation_bonus
        self.__multiplier_bonus: float = multiplier_bonus
        self.__is_activation_bonus_collected: bool = False

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, Generator) and \
            self.connected_doors == value.connected_doors and \
            self.active == value.active and \
            self.cost == value.cost and \
            self.activation_bonus == value.activation_bonus and \
            self.multiplier_bonus == value.multiplier_bonus

    @override
    @classmethod
    def from_ldtk_entity(cls, entity: EntityInstance, all_doors: dict[str, Door]) -> Self:
        cost: int = -1
        connected_doors: list[Door] = []
        activation_bonus: int = -1
        multiplier_bonus: float = -1.0
        for field in entity.field_instances:
            match field.identifier:
                case Generator.LDtkFieldIdentifiers.COST:
                    cost = field.value
                case Generator.LDtkFieldIdentifiers.CONNECTED_DOORS:
                    for ent in field.value:
                        iid = ent['entityIid']
                        if iid is None:
                            raise RuntimeError(f'could not find iid in {ent}')
                        door = all_doors.get(iid)
                        if door is None:
                            raise RuntimeError(f'could not find door (iid={iid})')
                        connected_doors.append(door)
                case Generator.LDtkFieldIdentifiers.ACTIVATION_BONUS:
                    activation_bonus = field.value
                case Generator.LDtkFieldIdentifiers.MULTIPLIER_BONUS:
                    multiplier_bonus = field.value

        return cls(cost=cost, doors=connected_doors, activation_bonus=activation_bonus, multiplier_bonus=multiplier_bonus)

    @override
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.__cost = data['cost']
        self.__active = data['active']
        self.__activation_bonus = data['activation_bonus']
        self.__multiplier_bonus = data['multiplier_bonus']
        self.__is_activation_bonus_collected = data['bonus_collected']
        self.connected_doors = [Door().from_json(d) for d in data['connected_doors']]
        return self

    @override
    def to_json(self) -> dict:
        jason = super().to_json()
        jason['cost'] = self.cost
        jason['active'] = self.active
        jason['connected_doors'] = [door.to_json() for door in self.connected_doors]
        jason['activation_bonus'] = self.activation_bonus
        jason['multiplier_bonus'] = self.multiplier_bonus
        jason['bonus_collected'] = self.is_activation_bonus_collected 
        return jason

    @override
    def take_action(self, avatar: Avatar) -> Item | None:
        if self.active:
            return
        # total_scrap = sum(map(lambda item: item.quantity if isinstance(item, Scrap) else 0, avatar.inventory))
        total_scrap = 0
        for item in avatar.inventory:
            if not isinstance(item, Scrap):
                continue
            total_scrap += item.quantity
        if total_scrap < self.cost:
            return
        avatar.take(Scrap(quantity=self.cost))
        if not self.is_activation_bonus_collected:
            avatar.give_score(self.activation_bonus)
            self.__is_activation_bonus_collected = True
        self.__active = True
        self.__toggle_doors(True)

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
    def multiplier_bonus(self) -> float:
        return self.__multiplier_bonus

    @property
    def activation_bonus(self) -> int:
        return self.__activation_bonus

    @property
    def is_activation_bonus_collected(self) -> bool:
        return self.__is_activation_bonus_collected

    # allows generators to be turned OFF by attacks
    def deactivate(self):
        """Force generator offline (doors remain unchanged)."""
        if not self.__active:
            return
        self.__active = False

    def activate(self):
        """Turn generator on (used for testing)."""
        self.__active = True

    def __toggle_doors(self, open: bool):
        for door in self.connected_doors:
            door.open = open
