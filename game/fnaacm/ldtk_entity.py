from abc import ABC, abstractmethod
from typing import Self

from game.utils import ldtk_json


class LDtkEntity(ABC):
    @classmethod
    @abstractmethod
    def from_ldtk_entity(cls, entity: ldtk_json.EntityInstance, *args, **kwargs) -> Self:
        ...
