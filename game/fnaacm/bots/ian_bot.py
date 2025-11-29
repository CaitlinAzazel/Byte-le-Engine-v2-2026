from typing import List, Optional
from game.fnaacm.bots.bot import Bot
from game.common.enums import ActionType
from game.utils.vector import Vector
from game.controllers.pathfind_controller import a_star_path


class IANBot(Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.turn_delay = 2  # moves every 2 turns

    def __calc_next_move_hunt(self, gameboard, player) -> List[ActionType]:
        bot_pos = self.position
        player_pos = player.avatar.position

        path = a_star_path(
            start=bot_pos,
            goal=player_pos,
            world=gameboard,
            allow_vents=False
        )

        if not path or len(path) < 2:
            return []

        next_step = path[1]
        delta = next_step - bot_pos
        action = self._vector_to_action(delta)
        if not action:
            return []

        return [action, action] if self.boosted else [action]

    def boosting(self, value: bool):
        self.boosted = value

    def __calc_next_move_patrol(self, gameboard, player) -> List[ActionType]:
        return []  # IAN has no patrol in these tests

    def _vector_to_action(self, delta: Vector) -> Optional[ActionType]:
        if delta.x == 0 and delta.y == -1:
            return ActionType.MOVE_UP
        if delta.x == 0 and delta.y == 1:
            return ActionType.MOVE_DOWN
        if delta.x == -1 and delta.y == 0:
            return ActionType.MOVE_LEFT
        if delta.x == 1 and delta.y == 0:
            return ActionType.MOVE_RIGHT
        return None
