from game.common.map.occupiable import Occupiable
from game.common.enums import ObjectType

class Vent(Occupiable):
    def __init__(self):
        super().__init__()
        self.object_type: ObjectType = ObjectType.VENT
