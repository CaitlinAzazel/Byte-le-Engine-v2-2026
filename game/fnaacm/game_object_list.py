from typing import Callable, Generic, Self, TypeVar
from game.common.game_object import GameObject

T = TypeVar('T', bound=GameObject)

class GameObjectList(GameObject, Generic[T]):
    """
    generic list wrapper that can store GameObjects
    """

    def __init__(self, json_key: str, constructor: Callable[..., T]):
        """
        :param json_key: the key that the contents of the list will be associated with when serialized
        :param constructor: the constructor method of T
        """
        super().__init__()

        # json_key and factory should be statically associated with the subclass somehow
        # not sure if possible

        self.__list_json_key: str = json_key
        # needed since we can't directly call the constructor of T
        # we will use this when deserializing the list's elements in from_json
        self.__constructor: Callable[..., T] = constructor
        self.__list: list[T] = []


    def __iter__(self):
        return iter(self.__list)

    def append(self, obj: T):
        self.__list.append(obj)

    def clear(self):
        self.__list.clear()

    def size(self) -> int:
        return len(self.__list)

    def get(self, index: int) -> T:
        return self.__list[index]

    def to_json(self) -> dict:
        data: dict = super().to_json()
        data[self.__list_json_key] = [game_object.to_json() for game_object in self.__list]
        return data

    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.__list = [self.__constructor().from_json(game_object_data) for game_object_data in data[self.__list_json_key]]
        return self
