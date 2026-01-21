from game.common.avatar import Avatar
from game.common.enums import ActionType, ObjectType
from game.common.map.game_board import GameBoard
from game.common.stations.refuge import Refuge
from game.controllers.controller import Controller


class PointController(Controller):
    """
    gives the player points when applicable
    """

    BASE_POINTS_PER_TURN = 1
    VENT_POINT_MULTIPLIER_REDUCTION = 0.5

    def __init__(self, base_points_per_turn: int = BASE_POINTS_PER_TURN):
        super().__init__()
        self.base_multiplier: float = 1.0
        self.__base_points_per_turn: int = base_points_per_turn

    @property
    def base_points_per_turn(self) -> int:
        return self.__base_points_per_turn

    def calculate_points(self, avatar: Avatar, world: GameBoard) -> int:
        result = self.base_points_per_turn

        generator_bonuses = [generator.passive_point_bonus for generator in world.generators.values() if generator.active]
        result += sum(generator_bonuses)

        return result

    def calculate_multiplier(self, avatar: Avatar, world: GameBoard) -> float:
        result = self.base_multiplier

        in_vent = len(world.get_objects_from(avatar.position, ObjectType.VENT)) > 0
        if in_vent:
            result -= PointController.VENT_POINT_MULTIPLIER_REDUCTION

        return result

    def handle_actions(self, avatar: Avatar, world: GameBoard):
        # no points if in refuge
        if Refuge.global_occupied:
            return

        points = round(self.calculate_points(avatar, world) * self.calculate_multiplier(avatar, world))
        avatar.give_score(points)
