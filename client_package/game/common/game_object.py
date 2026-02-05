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

    def obfuscate(self):
        ...
