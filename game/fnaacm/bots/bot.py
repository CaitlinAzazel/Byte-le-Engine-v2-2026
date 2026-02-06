from typing import Self, override
from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.utils.vector import Vector
from game.fnaacm.timer import Timer



class Bot(GameObject):
    DEFAULT_STUN_DURATION = 5
    DEFAULT_VISION_RADIUS = 1
    SAVED_PRIMITIVE_FIELDS = {'boosted', 'has_attacked', 'can_see_player', 'direction'}

    global_stun_turns_remaining = 0

    def __init__(self, stun_duration : int = DEFAULT_STUN_DURATION, start_position : Vector = Vector(), vision_radius: int = DEFAULT_VISION_RADIUS):
        super().__init__()
        self.object_type = ObjectType.BOT
        self.boosted : bool = False
        self.position : Vector = start_position
        self.vision_radius: int = vision_radius
        self.boosted_vision_radius: int = vision_radius * 2
        # Removed in exchange for global stun
        # self.stun_timer: Timer = Timer(stun_duration)
        self.has_attacked: bool = False
        self.can_see_player: bool = False # to be updated by `BotVisionController`
        self.turn_delay: int = 1
        self.direction: str = "" # to be updated by `BotMovementController`, used in visualizer


    def get_current_vision_radius(self) -> int:
        return self.boosted_vision_radius if self.boosted else self.vision_radius

    def can_attack(self, avatar: Avatar) -> bool:
        # distance check is just a shortcut for checking up/down/left/right
        return self.can_see_player and self.position.distance(avatar.position) <= 1 and not self.is_stunned

    def boosting(self, boost):
        self.boosted = boost

    @property
    def is_stunned(self) -> bool:
        return Bot.global_stun_turns_remaining > 0


    # available for backwards compatibility
    #@is_stunned.setter
    #def is_stunned(self, value: bool) -> None:
    #    if value:
    #        self.stun_timer.reset()
    #    else:
    #        self.stun_timer.force_done()


    #def stunned(self):
    #   self.stun_timer.tick()

    @classmethod
    def tick_global_stun(cls):
        # Decrements global stun counter, once per turn
        if cls.global_stun_turns_remaining > 0:
            cls.global_stun_turns_remaining -= 1

    def can_move(self, turn: int) -> bool:
        # turns are 1-indexed
        return (turn-1) % self.turn_delay == 0 and not self.is_stunned

    def attack(self, target: Avatar):
        """
        Perform an attack on the target Avatar.
        Tests expect:
        - bot.has_attacked becomes True
        - target receives the attack via target.receive_attack(bot)
        """
        if target is None:
            return

        # Avatar defines receive_attack()
        target.receive_attack()

        # Bot stunned after hitting the player
        Bot.global_stun_turns_remaining = Bot.DEFAULT_STUN_DURATION

        self.has_attacked = True

    def in_vision_radius(self, pos: Vector) -> bool:
        radius = self.get_current_vision_radius()
        top_left = self.position - Vector(radius, radius)
        bottom_right = self.position + Vector(radius, radius)

        if top_left.x <= pos.x <= bottom_right.x and \
            top_left.y <= pos.y <= bottom_right.y:
            return True
        return False

    @override
    def to_json(self) -> dict:
        if self.has_attacked:
            self.state = 'attacking'
        elif self.is_stunned:
            self.state = 'stunned'

        data = super().to_json()

        for field in Bot.SAVED_PRIMITIVE_FIELDS:
            assert hasattr(self, field)
            data[field] = getattr(self, field)

        data['position'] = self.position.to_json()
        data['global_stun_turns_remaining'] = Bot.global_stun_turns_remaining

        return data

    @override
    def from_json(self, data: dict) -> Self:
        super().from_json(data)

        for field in Bot.SAVED_PRIMITIVE_FIELDS:
            assert hasattr(self, field)
            setattr(self, field, data[field])

        self.position = Vector().from_json(data['position'])
        if 'global_stun_turns_remaining' in data:
            Bot.global_stun_turns_remaining = data['global_stun_turns_remaining']

        return self
