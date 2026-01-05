from game.common.avatar import Avatar
from game.common.enums import ObjectType
from game.common.game_object import GameObject
# from game.common.map.game_object_container import GameObjectContainer
from game.common.map.occupiable import Occupiable
from game.utils.vector import Vector



class Bot(GameObject):
    DEFAULT_STUN_DURATION = 5
    DEFAULT_VISION_RADIUS = 1

    def __init__(self, stun_duration : int = DEFAULT_STUN_DURATION, start_position : Vector = Vector(), vision_radius: int = DEFAULT_VISION_RADIUS):
        super().__init__()
        self.object_type = ObjectType.BOT
        self.boosted : bool = False
        self.is_stunned : bool = False
        self.position : Vector = start_position
        self.vision_radius: int = vision_radius
        self.boosted_vision_radius: int = vision_radius * 2
        self.stun_counter: int = 0
        self.has_attacked: bool = False
        self.can_see_player: bool = False # to be updated by `BotVisionController`
        self.turn_delay: int = 0

    def get_current_vision_radius(self) -> int:
        return self.boosted_vision_radius if self.boosted else self.vision_radius

    def can_attack(self, avatar: Avatar) -> bool:
        # distance check is just a shortcut for checking up/down/left/right
        return self.can_see_player and self.position.distance(avatar.position) <= 1

    def boosting(self, boost):
        self.boosted = boost

    def stunned(self):
        """do nothing"""
        self.stun_counter += 1
        if self.stun_counter == 5:
            self.is_stunned = False
            self.stun_counter = 0
        return

    def can_act(self, turn: int) -> bool:
        return turn % 2 == 0


    def attack(self, target):
        """
        Perform an attack on the target Avatar.
        Tests expect:
        - bot.has_attacked becomes True
        - target receives the attack via target.receive_attack(bot)
        """
        if target is None:
            return

        # Avatar defines receive_attack()
        if hasattr(target, "receive_attack"):
            target.receive_attack(self)

        # Bot stunned after hitting the player
        self.is_stunned = True
        self.stun_counter = 0

        self.has_attacked = True
