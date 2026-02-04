from game.common.map.occupiable import Occupiable
from game.common.enums import ObjectType


class Tile(Occupiable):
    """
    `Tile Class Notes:`

        Tiles are used as a placeholder object when generating the GameBoard.

        When the GameBoard is generated, it's specified where certain objects need to go. However, not every space on
        the map may have something there. If that is the case, a Tile is used to ensure `None` values are avoided.
        ^ this is just not true btw

        When something is meant to be placed on a Tile object, it will simply be appended to it.

        Here is an example:

            Current: [Tile]
            Object to place: Station
            Result: [Tile, Station]

        The additional objects are appended since it's more time efficient.

        Tiles are a great way to represent the floor when nothing else is present, but once something else should be
        there, that should be the focus.

        If the game being developed requires different tiles with special properties, future classes may be added and
        inherit from this class, and the rule about the Tile objects being replaced can always be removed.
    """
    def __init__(self):
        super().__init__()
        self.object_type: ObjectType = ObjectType.TILE
