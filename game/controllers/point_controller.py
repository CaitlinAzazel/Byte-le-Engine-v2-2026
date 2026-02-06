from dataclasses import dataclass
import dataclasses

from game.common.avatar import Avatar
from game.common.enums import ActionType, ObjectType
from game.common.map.game_board import GameBoard
from game.common.stations.refuge import Refuge
from game.controllers.controller import Controller


@dataclass
class PointData:
    points_generated: int = 0 
    multiplier: float = 0.0
    point_sources: dict[str, int] = dataclasses.field(default_factory=dict)
    multiplier_sources: dict[str, float] = dataclasses.field(default_factory=dict)

    @property
    def point_award(self) -> int:
        return round(self.points_generated * self.multiplier)

class PointController(Controller):
    """
    gives the player points when applicable
    """

    BASE_POINTS_PER_TURN = 100
    VENT_POINT_MULTIPLIER_REDUCTION = 0.5

    def __init__(self, base_points_per_turn: int = BASE_POINTS_PER_TURN):
        super().__init__()
        self.base_multiplier: float = 1.0
        self.__base_points_per_turn: int = base_points_per_turn

    @property
    def base_points_per_turn(self) -> int:
        return self.__base_points_per_turn

    def calculate_points(self, avatar: Avatar, world: GameBoard, point_data: PointData | None = None) -> int:
        """
        points to award BEFORE multiplier
        """
        result = self.base_points_per_turn

        if point_data is not None:
            point_data.point_sources['alive'] = self.base_points_per_turn

        return result

    def calculate_multiplier(self, avatar: Avatar, world: GameBoard, point_data: PointData | None = None) -> float:
        assert avatar.position is not None
        if Refuge.global_occupied:
            if point_data is not None:
                point_data.multiplier_sources['in_refuge'] = 0.0
            return 0.0

        result = self.base_multiplier

        generator_bonuses = sum([generator.multiplier_bonus for generator in world.generators.values() if generator.active])
        if generator_bonuses > 0 and point_data is not None:
            point_data.multiplier_sources['generators'] = generator_bonuses
        result += generator_bonuses

        in_vent = len(world.get_objects_from(avatar.position, ObjectType.VENT)) > 0
        if in_vent:
            result -= PointController.VENT_POINT_MULTIPLIER_REDUCTION
            if point_data is not None:
                point_data.multiplier_sources['in_vent'] = -PointController.VENT_POINT_MULTIPLIER_REDUCTION

        return result

    def handle_actions(self, avatar: Avatar, world: GameBoard) -> PointData:
        point_data = PointData()
        points_generated = self.calculate_points(avatar, world, point_data)
        point_data.points_generated = points_generated
        point_multiplier = self.calculate_multiplier(avatar, world, point_data)
        point_data.multiplier = point_multiplier

        avatar.give_score(point_data.point_award)

        return point_data
