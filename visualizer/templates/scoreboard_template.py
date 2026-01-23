import pygame
from game.utils.vector import Vector
from game.config import MAX_TICKS
from visualizer.utils.text import Text
from visualizer.templates.info_template import InfoTemplate


class ScoreboardTemplate(InfoTemplate):
    """
    Displays the game scoreboard: current score and turn counter.
    """

    def __init__(self, screen: pygame.Surface, topleft: Vector, size: Vector, font: str, color: str) -> None:
        super().__init__(screen, topleft, size, font, color)

        # Single score display
        self.score: Text = Text(
            screen,
            text="0",
            font_size=36,
            font_name=font,
            color=color,
            position=Vector(topleft.x + 50, topleft.y)
        )

        # Turn counter: current turn / max turns
        self.turn: Text = Text(
            screen,
            text=f"0 / {MAX_TICKS}",
            font_size=36,
            font_name=font,
            color=color,
            position=Vector(topleft.x + 400, topleft.y)
        )

        # Scrap display
        self.scrap: Text = Text(
            screen,
            text="Scrap: 0",
            font_size=36,
            font_name=font,
            color=color,
            position=Vector(topleft.x + 600, topleft.y)
        )

        # Store current values for updates
        self.current_scrap = 0
        self.current_score = 0
        self.current_turn = 0

    def recalc_animation(self, turn_log: dict) -> None:
        """
        Update the score and turn each frame.
        Expects turn_log to contain:
          - 'tick': current turn
          - 'score': current score (or sum of team scores)
        """

        # Update score
        if 'clients' in turn_log:
            # Sum all client scores and total scrap
            self.current_score = sum(
                client['avatar']['score'] if client.get('avatar') else 0
                for client in turn_log['clients']
            )

            self.current_scrap = sum(
                client['avatar']['scrap'] if client.get('avatar') else 0
                for client in turn_log['clients']
            )
        else:
            self.current_score = turn_log.get('score', 0)

        # Update turn
        self.current_turn = turn_log.get('tick', 0)

        # Update Text objects
        self.score.text = f"Score: {self.current_score}"
        self.turn.text = f"{self.current_turn} / {MAX_TICKS}"
        self.scrap.text = f"Scrap: {self.current_scrap}"

    def render(self) -> None:
        """
        Draw the score, scrap, and turn counter on the screen.
        """
        self.score.render()
        self.turn.render()
        self.scrap.render()
