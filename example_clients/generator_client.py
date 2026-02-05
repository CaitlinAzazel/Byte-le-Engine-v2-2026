import random

from game.client.user_client import UserClient
from game.common.avatar import Avatar
from game.common.enums import ObjectType, ActionType
from game.common.map.game_board import GameBoard
from game.common.map.occupiable import Occupiable
from game.utils.vector import Vector
from game.constants import *

class Client(UserClient):

    def __init__(self):
        super().__init__()
        self.goal: Vector = Vector()

    def team_name(self) -> str:
        """
        Allows the team to set a team name.
        :return: Your team name
        """
        return "William Afton"

    def take_turn(self, turn: int, world: GameBoard, avatar: Avatar) -> list[ActionType]:
        """
        This is where your AI will decide what to do.
        :param turn:        The current turn of the game.
        :param world:       Generic world information
        :param avatar:      Your in-game character
        """
        actions: list[ActionType] = []
        current: Vector = avatar.position

        goal_object = ObjectType.COIN_SPAWNER
        held_scrap = avatar.get_quantity_of_item_type(ObjectType.SCRAP)
        if held_scrap > 0:
            goal_object = ObjectType.GENERATOR
        else:
            goal_object = ObjectType.SCRAP_SPAWNER

        goals = world.get_objects(goal_object).copy()
        if not goals:
            return actions

        if goal_object == ObjectType.GENERATOR:
            temp = dict()
            for pos, go_container in goals.items():
                if len(go_container) < 1:
                    continue
                obj = go_container[-1]
                if not hasattr(obj, 'active'):
                    # shouldnt happen
                    continue
                active = getattr(obj, 'active', False)
                if not active:
                    temp[pos] = go_container
            goals = temp

        goal = min(goals.keys(), key=current.distance)
        if goal != self.goal:
            # print(f'\tset goal {goal}')
            self.goal = goal
        move = self.step_toward(world, current, goal, avatar)
        if move:
            actions.append(move)

        for pos, gen in world.generators.items():
            if gen.active:
                continue
            if current.distance(pos) <= 1:
                # print(f'close to generator')
                actions.append(DIRECTION_TO_INTERACT[pos - current])
                break

        return actions

    def step_toward(self, world: GameBoard, current: Vector, goal: Vector, avatar: Avatar):
        best_move = None
        best_dist = current.distance(goal)

        for action, direction in sorted(MOVE_TO_DIRECTION.items(), key=lambda _: random.random()):
            next = current + direction

            if not world.can_object_occupy(next, avatar):
                continue

            dist = next.distance(goal)
            if dist < best_dist:
                best_dist = dist
                best_move = action

        return best_move

