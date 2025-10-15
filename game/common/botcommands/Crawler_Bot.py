from game.common.botcommands.General_Bot_Commands import *
from game.common.avatar import Avatar
from game.controllers.master_controller import MasterController
from game.common.map.game_board import GameBoard
import heapq
from game.common.enums import ObjectType
from game.utils.vector import Vector


class CrawlBot:
    def __init__(self):
        super().__init__()
        self.vision = 1
        self.movement_controller: MovementController = MovementController()
        self.master_controller: MasterController = MasterController()
        self.game_board: GameBoard = GameBoard()
        self.player_seen : bool = False
        self.boosted : bool = False
        self.avatar: Avatar = Avatar()
        self.playerX: 0
        self.playerY: 0
        self.stun = False
        self.stun_counter = 0
        self.object_type = ObjectType.AVATAR
        self.turn_counter = 0
        self.position = Avatar.position

    def a_star(self, board, start: Vector, goal: Vector) -> list[Vector]:
        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        visited = set()

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            visited.add(current)

            for neighbor in self.get_neighbors(current, board):
                if neighbor in visited:
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return [start]  # No path found

    def get_neighbors(self, pos: Vector, board) -> list[Vector]:
        directions = [Vector(0, 1), Vector(0, -1), Vector(1, 0), Vector(-1, 0)]
        neighbors = []

        for d in directions:
            neighbor = pos + d
            if board.is_valid_coords(neighbor) and board.is_occupiable(neighbor):
                neighbors.append(neighbor)

        return neighbors

    def heuristic(self, a: Vector, b: Vector) -> int:
        # Manhattan distance
        return abs(a.x - b.x) + abs(a.y - b.y)

    def reconstruct_path(self, came_from: dict, current: Vector) -> list[Vector]:
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.insert(0, current)
        return path

    def stunned(self):
        """do nothing"""
        self.stun_counter += 1
        if self.stun_counter == 5:
            self.stun = False
            self.stun_counter = 0
        return

    def boosting(self, boost):
        self.boosted = boost

    def action(self, game_board, player_avatar):
        self.turn_counter += 1

        if self.boosted:
            if self.turn_counter % 2 != 0:
                return  # Only act every other turn
        else:
            if self.turn_counter % 4 != 0:
                return  # Only act every 4 turns

        if not self.position or not player_avatar.position:
            return

        path = self.a_star(game_board, self.position, player_avatar.position)

        if len(path) > 1:
            next_step = path[1]
            if game_board.is_occupiable(next_step):
                game_board.remove(self.position, self.object_type)
                game_board.place(next_step, self)
                self.position = next_step