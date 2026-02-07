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

        self.health_text: Text = Text(
            screen,
            text="HP: 0",
            font_size=36,
            font_name=font,
            color=color,
            position=Vector(topleft.x + 800, topleft.y)
        )

        self.power_text: Text = Text(
            screen,
            text="Power:   0%",
            font_size=36,
            font_name=font,
            color=color,
            position=Vector(topleft.x + 1000, topleft.y)
        )

        self.team_name_text: Text = Text(
            screen,
            text="Your Team Name",
            font_size=36,
            font_name=font,
            color=color,
        )
        # self.fastest_speed_button.rect.center = screen_center.add_x_y(200, 350).as_tuple()
        self.team_name_text.rect.center = Vector.from_xy_tuple(screen.get_rect().center).add_x_y(380, 340).as_tuple()
        

        # Store current values for updates
        self.current_scrap = 0
        self.current_score = 0
        self.current_turn = 0
        self.current_health = 0
        self.current_power = 0

    def recalc_animation(self, turn_log: dict) -> None:
        """
        Update the score and turn each frame.
        Expects turn_log to contain:
          - 'tick': current turn
          - 'score': current score (or sum of team scores)
        """

        team_name: str = ''
        # Update score
        if 'clients' in turn_log:
            team_name = turn_log['clients'][0]['team_name']
            # Sum all client scores and total scrap
            def sum_avatar_attr(attr: str):
                return sum(
                    client['avatar'][attr] if client.get('avatar') else 0
                    for client in turn_log['clients']
                )

            self.current_score = sum_avatar_attr('score')
            self.current_scrap = sum_avatar_attr('scrap')
            self.current_health = sum_avatar_attr('health')
            self.current_power = sum_avatar_attr('power')
        else:
            self.current_score = turn_log.get('score', 0)

        # Update turn
        self.current_turn = turn_log.get('tick', 0)

        # Update Text objects
        self.score.text = f"Score: {self.current_score}"
        self.turn.text = f"{self.current_turn} / {MAX_TICKS}"
        self.scrap.text = f"Scrap: {self.current_scrap}"
        self.health_text.text = f"HP: {self.current_health}"
        self.power_text.text = f"Power: {self.current_power:3}%"
        TEAM_NAME_TRUNCATE_CHAR_LIMIT = 18
        if len(team_name) > TEAM_NAME_TRUNCATE_CHAR_LIMIT:
            team_name = team_name[:TEAM_NAME_TRUNCATE_CHAR_LIMIT-3] + '...'
        self.team_name_text.text = f"{team_name}"

    def render(self) -> None:
        """
        Draw the score, scrap, and turn counter on the screen.
        """
        self.score.render()
        self.turn.render()
        self.scrap.render()
        self.health_text.render()
        self.power_text.render()
        self.team_name_text.render()
