from typing import Self, override
from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.utils.vector import Vector
from game.fnaacm.timer import Timer



class Bot(GameObject):
    DEFAULT_STUN_DURATION = 0
    DEFAULT_VISION_RADIUS = 0

    def __init__(self, stun_duration : int = DEFAULT_STUN_DURATION, start_position : Vector = Vector(), vision_radius: int = DEFAULT_VISION_RADIUS):
        super().__init__()
        self.object_type = ObjectType.BOT
        self.boosted : bool = False
        self.position : Vector = start_position
        self.vision_radius: int = vision_radius
        self.boosted_vision_radius: int = vision_radius * 2
        self.stun_timer: Timer = Timer(stun_duration)
        self.has_attacked: bool = False
        self.can_see_player: bool = False # to be updated by `BotVisionController`
        self.turn_delay: int = 1
        self.direction: str = "" # to be updated by `BotMovementController`, used in visualizer

    def get_current_vision_radius(self) -> int:
        ...

    def can_attack(self, avatar: Avatar) -> bool:
        ...

    def boosting(self, boost):
        ...

    @property
    def is_stunned(self) -> bool:
        ...

    def stunned(self):
        ...

    def can_move(self, turn: int) -> bool:
        ...

    def attack(self, target: Avatar):
        """
        Perform an attack on the target Avatar.
        Tests expect:
        - bot.has_attacked becomes True
        - target receives the attack via target.receive_attack(bot)
        """
        ...

    def in_vision_radius(self, pos: Vector) -> bool:
        ...
