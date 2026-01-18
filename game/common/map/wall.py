from typing import Self
from game.common.enums import ObjectType
from game.common.game_object import GameObject


class Wall(GameObject):
    """
    `Wall Class Note:`

        The Wall class is used for creating objects that border the map. These are impassable.
    """
    def __init__(self, use_shadow_sprite: bool = False):
        super().__init__()
        self.object_type = ObjectType.WALL
        self.use_shadow_sprite = use_shadow_sprite
    
    def from_json(self, data: dict) -> Self:
        super().from_json(data)
        self.use_shadow_sprite = data['use_shadow_sprite']
        return self

    def to_json(self) -> dict:
        data = super().to_json()
        data['use_shadow_sprite'] = self.use_shadow_sprite
        return data
