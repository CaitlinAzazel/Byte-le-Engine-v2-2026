from typing import Any

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from game.utils.vector import Vector
from visualizer.utils.button import Button, ButtonColors
from visualizer.utils.text import Text

"""
This is file is for creating different templates for the start menu of the visualizer. Each different menu screen 
will be a different class. The Basic class is the default template for the screen. Create extra classes for 
different start menu screens. The Basic class can be used as a template on how to do so.
"""


class MenuTemplate:
    """
    Menu Template is used as an interface. It provides a screen object from pygame.Surface, a 'Start Game' and
    'Exit' button. These are common attributes to all menus, so they are provided to facilitate creating them. Any
    other buttons should be created.

    This class also provides methods that are expanded upon in the Basic class, which is also in this file. Refer to
    that class' documentation for further detail. These provided methods can be used via inheritance and expanded upon
    as needed.

    NOTE: The provided buttons are already made to be in the center of the screen.
    """

    def __init__(self, screen: pygame.Surface):
        self.screen: pygame.Surface = screen  # captures the screen in an object
        self.start_button: Button = Button(screen, 'Start Game', lambda: False, font_size=24, padding=10)
        self.results_button: Button = Button(screen, 'Exit', lambda: False, font_size=24, padding=10)

        # the next two variables shouldn't be type hinted. The center is a tuple of two ints (i.e., tuple[int, int])
        self.start_button.rect.center = Vector(*self.screen.get_rect().center).add_y(100).as_tuple()

        self.results_button.rect.center = Vector(*self.screen.get_rect().center).add_y(100).as_tuple()

    def start_events(self, event: pygame.event) -> Any:
        """
        This method will return if the user presses the 'Start Game' button. The return type is Any since that's what
        the `mouse_clicked()` method returns.
        :param event:
        :return: Any
        """
        return self.start_button.mouse_clicked(event) if self.start_button.mouse_clicked(
            event) is not None else True

    def start_render(self) -> None:
        """
        Renders the Start button.
        :return: None
        """

        def start_render(self) -> None:
            # Draw background image first
            self.screen.blit(self.background, (0, 0))

            # Draw buttons and title on top
            super().start_render()
            self.title.render()

    def load_results_screen(self, results: dict): ...

    def results_events(self, event: pygame.event) -> Any:
        """
        This method will return if the user presses the 'Exit' button on the results screen. The return type is Any
        since that's what the `mouse_clicked()` method returns.
        :param event:
        :return: Any
        """
        return self.results_button.mouse_clicked(event) if self.results_button.mouse_clicked(
            event) is not None else True

    def results_render(self) -> None:
        """
        Renders the Results button.
        :return: None
        """
        self.results_button.render()


class Basic(MenuTemplate):
    """
    The Basic class is a default template that can be used for the menu screens. It inherits from MenuTemplate and
    expands on the inherited methods. If different templates are desired, create more classes in this file. This
    Basic class can be used as a template for any future classes.
    """

    def __init__(self, screen: pygame.Surface, title: str):
        super().__init__(screen)
        self.title: Text = Text(screen, title, 48)
        self.title.rect.center = Vector(*self.screen.get_rect().center).add_x_y(-100, -100).as_tuple()
        self.winning_team_name: Text = Text(screen, '', 0)

        # START MENU IMAGE
        self.background = pygame.image.load(
            os.path.join(os.getcwd(), "visualizer/images/staticsprites/StartMenu.png")
        ).convert_alpha()
        self.background = pygame.transform.smoothscale(self.background, self.screen.get_size())

        menu_colors = ButtonColors(
            fg_color="#ffffff",  # White text
            fg_color_hover="#ffff00",  # Yellow text on hover
            fg_color_clicked="#00ff00",  # Green text when clicked
            bg_color="#333399",  # Dark purple background
            bg_color_hover="#6666cc",  # Lighter purple on hover
            bg_color_clicked="#111166"  # Darker purple when clicked
        )

        # Recreate Start Button with colors and position
        self.start_button = Button(
            screen=self.screen,
            text="Start Game",
            action=lambda: False,  # Replace with actual start function
            font_size=24,
            padding=12,
            colors=menu_colors,
            position=Vector(self.screen.get_width() // 2 - 500, self.screen.get_height() // 2 + 50)
        )

        # Recreate Exit Button with colors and position
        self.results_button = Button(
            screen=self.screen,
            text="Exit",
            action=lambda: False,  # Replace with actual exit function
            font_size=24,

            padding=12,
            colors=menu_colors,
            position=Vector(self.screen.get_width() // 2 - 500, self.screen.get_height() // 2 + 120)
        )

    def start_render(self) -> None:
        """
        This method calls the inherited method to render the start button. It also renders the title
        :return: None
        """

        self.screen.blit(self.background, (0, 0))
        self.start_button.render()
        self.results_button.render()
        super().start_render()

    def load_results_screen(self, results: dict) -> None:
        """
        This method will update the self.winning_team_name variable based on the results dict given.
        :param results:
        :return: None
        """
        winning_teams = self.__get_winning_teams(results['players'])
        self.winning_team_name = Text(self.screen, winning_teams, 36, color=(255, 0, 0))
        self.winning_team_name.rect.center = Vector(*self.screen.get_rect().center).add_x(-425).as_tuple()


    def results_render(self) -> None:
        """
        This renders the results screen by placing the title and winning team name(s) on the screen.
        :return:
        """
        super().results_render()
        self.screen.blit(self.background, (0, 0))
        self.winning_team_name.render()
        self.results_button.render()

    def __get_winning_teams(self, players: list) -> str:
        """
        This method will get the winning team name(s) and return that string. If there is a tie, all teams that created
        the tie will be included.
        :param players:
        :return: string with the winning team name(s)
        """
        m = max(map(lambda player: player['avatar']['score'], players))  # Gets the max score from all results

        # Compares each player in the given list to the max score
        winners: list = [player['team_name'] for player in players if player['avatar']['score'] == m]

        # Prints the winner(s) from the final results
        return f'{"Winners" if len(winners) > 1 else "Winner"}: {", ".join(winners)}'
