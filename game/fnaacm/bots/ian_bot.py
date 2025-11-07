# ian_bot.py
from typing import Optional, Tuple, List, Dict
import heapq

from game.fnaacm.bots.bot import Bot
from game.controllers.attack_controller import Attack_Controller
from game.common.enums import ActionType, ObjectType
from game.utils.vector import Vector
from game.common.map.wall import Wall
from game.common.map.occupiable import Occupiable


Position = Tuple[int, int]


def _vec_to_pos(v: Vector) -> Position:
    return (v.x, v.y)


def _pos_to_vec(p: Position) -> Vector:
    return Vector(p[0], p[1])


def _neighbors(pos: Position) -> List[Position]:
    x, y = pos
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def _heuristic(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _a_star(world, start: Position, goal: Position, allow_vents: bool = False) -> Optional[List[Position]]:
    """A* search over the gameboard using world.get_top() and world.is_valid_coords()."""
    if start == goal:
        return [start]

    frontier: List[Tuple[int, Position]] = []
    heapq.heappush(frontier, (0, start))
    came_from: Dict[Position, Optional[Position]] = {start: None}
    cost_so_far: Dict[Position, int] = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            # reconstruct
            path: List[Position] = []
            cur = current
            while cur is not None:
                path.append(cur)
                cur = came_from[cur]
            path.reverse()
            return path

        for nxt in _neighbors(current):
            nx, ny = nxt
            vec = _pos_to_vec(nxt)
            # bounds check
            if not world.is_valid_coords(vec):
                continue

            top = world.get_top(vec)
            # impassable: wall objects
            if top is not None and getattr(top, "object_type", None) == ObjectType.WALL:
                continue

            # vent handling
            if top is not None and getattr(top, "object_type", None) == ObjectType.VENT and not allow_vents:
                continue

            # If top exists and is not Occupiable, skip
            if top is not None and not isinstance(top, Occupiable):
                # e.g., another bot or non-occupiable object; treat as blocked
                continue

            new_cost = cost_so_far[current] + 1
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                priority = new_cost + _heuristic(goal, nxt)
                heapq.heappush(frontier, (priority, nxt))
                came_from[nxt] = current

    return None


class IANBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.turn_delay = 2
        self.attack_controller = Attack_Controller()

    def should_move(self, turn_number: int) -> bool:
        return (turn_number % self.turn_delay) == 0

    def _cardinal_attack_action(self, dx: int, dy: int) -> Optional[ActionType]:
        if dx == 0 and dy == -1:
            return ActionType.ATTACK_UP
        if dx == 0 and dy == 1:
            return ActionType.ATTACK_DOWN
        if dx == -1 and dy == 0:
            return ActionType.ATTACK_LEFT
        if dx == 1 and dy == 0:
            return ActionType.ATTACK_RIGHT
        return None

    def _move_one_step_along_path(self, world, path: List[Position]) -> None:
        """Move the bot one tile along path (path is list of positions start..goal)."""
        if not path or len(path) < 2:
            return
        current_pos = _vec_to_pos(self.avatar.position)
        next_pos = path[1]
        next_vec = _pos_to_vec(next_pos)
        # perform move using GameBoard API (remove/place)
        # remove current
        world.remove(self.avatar.position, self.object_type)
        # place at destination
        world.place(next_vec, self)
        # set avatar position
        self.avatar.position = next_vec

    def take_turn(self, turn_number: int, player, world) -> None:
        """
        Finds player on the board, attempts to move or attack.
        Ian cannot use vents (allow_vents=False).
        """
        if player is None or world is None:
            return

        # if not this bot's movement turn, skip
        if not self.should_move(turn_number):
            return

        bot_pos = _vec_to_pos(self.avatar.position)
        player_pos = _vec_to_pos(player.avatar.position)

        dx = player_pos[0] - bot_pos[0]
        dy = player_pos[1] - bot_pos[1]

        # If adjacent in cardinal directions -> attack
        if abs(dx) + abs(dy) == 1:
            action = self._cardinal_attack_action(dx, dy)
            if action:
                self.attack_controller.handle_actions(action, player, world, self)
            return

        # Pathfind (no vents)
        path = _a_star(world, bot_pos, player_pos, allow_vents=False)
        if not path:
            return

        self._move_one_step_along_path(world, path)
