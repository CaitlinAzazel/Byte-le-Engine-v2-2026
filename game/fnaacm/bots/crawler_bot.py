from typing import List, Optional, override
from game.fnaacm.bots.bot import Bot
# from game.common.enums import ActionType
# from game.utils.vector import Vector
# from game.controllers.pathfind_controller import a_star_path


class CrawlerBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.turn_delay = 4  # moves every 4 turns unboosted
        self.vision_radius = 40
        self.boosted_vision_radius = 40

    # @override
    # def _calc_next_move_hunt(self, gameboard, player) -> List[ActionType]:
    #     bot_pos = self.position
    #     player_pos = player.avatar.position
    #
    #     path = a_star_path(
    #         start=bot_pos,
    #         goal=player_pos,
    #         world=gameboard,
    #         allow_vents=True  # crawler special rule
    #     )
    #
    #     if not path or len(path) < 2:
    #         return []
    #
    #     next_step: Vector = path[1]
    #     direction = next_step - bot_pos
    #     action = self._vector_to_action(direction)
    #     if not action:
    #         return []
    #
    #     return [action, action] if self.boosted else [action]
    #
    # @override
    # def _calc_next_move_patrol(self, gameboard, player) -> List[ActionType]:
    #     return []  # Crawler has no patrol
    #
    # def _vector_to_action(self, delta: Vector) -> Optional[ActionType]:
    #     if delta.x == 0 and delta.y == -1:
    #         return ActionType.MOVE_UP
    #     if delta.x == 0 and delta.y == 1:
    #         return ActionType.MOVE_DOWN
    #     if delta.x == -1 and delta.y == 0:
    #         return ActionType.MOVE_LEFT
    #     if delta.x == 1 and delta.y == 0:
    #         return ActionType.MOVE_RIGHT
    #     return None
