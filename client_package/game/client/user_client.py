from game.common.avatar import Avatar
from game.common.enums import *
from game.common.map.game_board import GameBoard
from game.config import Debug
import logging


class UserClient:
    def __init__(self):
        self.debug_level: DebugLevel = DebugLevel.CLIENT
        self.debug_enabled: bool = True

    def debug(self, *args) -> None:
        if self.debug_enabled and Debug.level.value >= self.debug_level.value:
            logging.basicConfig(level=logging.DEBUG)
            for arg in args:
                logging.debug(f'{self.__class__.__name__}: {arg}')

    def team_name(self) -> str:
        """
        :return: your team name
        """
        return "Your Team Name Here"

    def take_turn(self, turn: int, world: GameBoard, avatar: Avatar) -> list[ActionType]:
        raise NotImplementedError("Implement this in subclass")
