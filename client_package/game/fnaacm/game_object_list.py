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
        ...

    def clear(self):
        ...

    def size(self) -> int:
        ...

    def get(self, index: int) -> T:
        ...
