from game.common.enums import ObjectType


class GameObjectContainer(GameObject):
    """
    This class encapsulates all objects that are to be stored at a coordinate in the GameBoard.
    """

    def __init__(self, objects: list[GameObject] | None = None):
        super().__init__()
        self.object_type: ObjectType = ObjectType.GAME_OBJECT_CONTAINER
        self.__sublist: list[GameObject] = []
        self.place_all(objects)

    def __iter__(self):
        return iter(self.__sublist)

    def place_all(self, game_objs: list[GameObject] | None) -> bool:
        ...

    def place(self, game_obj: GameObject | None) -> bool:
        """
        Attempts to place the given GameObject on the given coordinate if the coordinate is valid. If the top-most
        object inherits from Occupiable, the given object will be placed. If the top-most object *doesn't* inherit
        from Occupiable, but the given object does, it will be placed below the unoccupiable object. If the neither
        the top-most object nor the given object inherit from Occupiable, it will not be placed. If the top-most object
        is a wall, nothing will be placed at all.

        Examples

        1:
            - Top of stack object: OccupiableStation1
            - Given: OcccupiableStation2
            - Result: OccupiableStation1 -> OccupiableStation2
                Success
        2:
            - Top of stack object: Avatar
            - Given: OccupiableStation
            - Result: OccupiableStation, Avatar
                Success
        3:
            - Top of stack object: Station
            - Given: Avatar
            - Result: Station
                Failure
        4:
            - Top of stack object: Wall
            - Given: Avatar
            - Result: Wall
                Failure

        NOTE: True and False are returned instead of raising an error to prevent misuse of these methods during the
        competition; if a competitor uses them and the game crashes, the game would end abruptly.

        :param game_obj:
        :return: True to represent a success, False to represent a failure
        """
        ...

    def remove(self, object_type: ObjectType) -> GameObject | None:
        """
        Removes the first instance of the given ObjectType from the valid coordinate. The removed object is returned if
        applicable.
        :param object_type:
        :return: removed GameObject or None
        """
        ...

    def get_top(self) -> GameObject | None:
        """
        returns None if:
            - the sublist is empty
            - the sublist is somehow None
        """
        ...

    def get_objects(self, object_type: ObjectType | None = None) -> list[GameObject]:
        """
        Gets all GameObjects of a specified type. If no parameter is provided, all objects are returned.
        :param object_type:
        :return: a list of GameObjects
        """
        ...

