from game.common.game_object import GameObject
from game.common.enums import ObjectType
from game.common.items.item import Item


# create Station object from GameObject that allows item to be contained in it
class Station(GameObject):
    """
    `Station Class Notes:`

        Station objects inherit from GameObject and can contain Item objects in them.

        Players can interact with Stations in different ways by using the ``take_action()`` method. Whatever is specified
        in this method will control how players interact with the station. The Avatar and Item classes have methods that
        go through this process. Refer to them for more details.

        The Occupiable Station Example class demonstrates an avatar object receiving the station's stored item. The
        Station Receiver Example class demonstrates an avatar depositing its held item into a station. These are simple
        ideas for how stations can be used. These can be heavily added onto for more creative uses!
    """

    def __init__(self, held_item: Item | None = None, **kwargs):
        super().__init__()
        self.object_type: ObjectType = ObjectType.STATION
        self.held_item: Item | None = held_item

    # held_item getter and setter methods
    @property
    def held_item(self) -> Item | None:
        return self.__item

    @held_item.setter
    def held_item(self, held_item: Item) -> None:
        if held_item is not None and not isinstance(held_item, Item):
            raise ValueError(f'{self.__class__.__name__}.held_item must be an Item or None, not {held_item}.')
        self.__item = held_item

