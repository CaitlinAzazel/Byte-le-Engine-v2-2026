import pygame

import game.config as gc
from game.utils.vector import Vector
from visualizer.templates.info_template import InfoTemplate


class ScoreboardTemplate(InfoTemplate):
    def __init__(self, screen: pygame.Surface, topleft: Vector, size: Vector, font: str, color: str) -> None:
        super().__init__(screen, topleft, size, font, color)

        # IMPLEMENT SCOREBOARD HERE (You can check out 2024/2025 scoreboard template for help)
        # https://github.com/acm-ndsu/Byte-le-2025/blob/main/visualizer/templates/scoreboard_template.py
        ...


    def recalc_animation(self, turn_log: dict) -> None:

        # RECALC SCORES PER TURN HERE
        ...
