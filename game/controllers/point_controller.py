from game.common.enums import ActionType
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.common.stations.refuge import Refuge
from game.controllers.controller import Controller


class PointController(Controller):
    """
    gives the player points when applicable
    """

    DEFAULT_POINTS_PER_TURN = 1

    def __init__(self, points_per_turn: int = DEFAULT_POINTS_PER_TURN):
        super().__init__()
        self.__multiplier = 1
        self.__points_per_turn = points_per_turn

    @property
    def points_per_turn(self) -> int:
        return self.__points_per_turn

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard):
        del action

        # no points if in refuge
        if Refuge.global_occupied:
            return

        # TODO: each generator increases point multiplier

        points = self.__points_per_turn * self.__multiplier 
        client.avatar.give_points(self.__points_per_turn)
