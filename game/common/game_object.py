import uuid

from game.common.enums import ObjectType
from typing import Self


class GameObject:
    """
    `GameObject Class Notes:`

        This class is widely used throughout the project to represent different types of Objects that are interacted
        with in the game. If a new class is created and needs to be logged to the JSON files, make sure it inherits
        from GameObject.
    """
    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        self.object_type = ObjectType.NONE
        self.state = "idle"

    @classmethod
    def new_from_json(cls, data: dict):
        return cls().from_json(data)

    def to_json(self) -> dict:
        # It is recommended call this using super() in child implementations
        data = dict()

        data['id'] = self.id
        data['object_type'] = self.object_type.value
        data['state'] = self.state

        data['__class__'] = self.__class__.__name__

        return data

    def from_json(self, data: dict) -> Self:
        # It is recommended call this using super() in child implementations
        self.id = data['id']
        self.object_type = ObjectType(data['object_type'])
        self.state = data['state']
        return self

    def obfuscate(self):
        pass
