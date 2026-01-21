from abc import ABC
from typing import Self

from game.utils import ldtk_json


class LDtkEntity(ABC):
    @classmethod
    def from_ldtk_entity(cls, entity: ldtk_json.EntityInstance) -> Self:
        ...
