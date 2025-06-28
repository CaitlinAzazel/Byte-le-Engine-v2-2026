from typing import Self
from game.common.game_object import GameObject
from game.fnaacm.stations.battery import Battery


class BatteryList(GameObject):
    """
    list wrapper that stores Batteries
    """
    def __init__(self):
        super().__init__()
        self.__list: list[Battery] = []

    def append(self, dynamite: Battery):
        self.__list.append(dynamite)

    def size(self) -> int:
        return len(self.__list)

    def get(self, index: int) -> Battery:
        return self.__list[index]

    def to_json(self) -> dict:
        data: dict = super().to_json()
        data['batteries'] = list(map(lambda battery: battery.to_json(), self.__list))
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.__list: list[Battery] = list(map(lambda battery: Battery().from_json(battery), data['batteries']))
        return self
