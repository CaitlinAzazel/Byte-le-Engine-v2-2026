import heapq
from typing import Dict, List, Tuple, Optional
from game.common.enums import ObjectType
from game.common.game_object import GameObject
from game.common.map.occupiable import Occupiable
from game.utils.vector import Vector

Position = Tuple[int, int]

DIRECTIONS = [(1,0), (-1,0), (0,1), (0,-1)]

def a_star_path(start: Vector, goal: Vector, world, allow_vents=True) -> Optional[List[Vector]]:
    start_p = (start.x, start.y)
    goal_p = (goal.x, goal.y)

    frontier = [(0, start_p)]
    came_from = {start_p: None}
    cost = {start_p: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal_p:
            path = []
            while current is not None:
                x, y = current
                path.insert(0, Vector(x, y))
                current = came_from[current]
            return path

        for dx, dy in DIRECTIONS:
            nxt = (current[0] + dx, current[1] + dy)
            vec = Vector(nxt[0], nxt[1])

            if not world.is_valid_coords(vec):
                continue

            top = world.get_top(vec)
            if top and top.object_type != ObjectType.AVATAR:
                # walls block
                if top.object_type == ObjectType.WALL:
                    continue

                # vents block unless allowed
                if top.object_type == ObjectType.VENT and not allow_vents:
                    continue

                # can't pass through non-occupiable
                if not isinstance(top, Occupiable):
                    continue

            new_cost = cost[current] + 1
            if nxt not in cost or new_cost < cost[nxt]:
                cost[nxt] = new_cost
                priority = new_cost + vec.distance(goal)
                heapq.heappush(frontier, (priority, nxt))
                came_from[nxt] = current

    return None
