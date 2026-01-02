import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from game.config import *
from typing import Callable, Any
from visualizer.bytesprites.tileBS import TileBS
from visualizer.bytesprites.wallBS import WallBS
from visualizer.bytesprites.avatarBS import AvatarBS
from game.utils.vector import Vector
from visualizer.utils.text import Text
from visualizer.bytesprites.bytesprite import ByteSprite
from visualizer.templates.menu_templates import Basic, MenuTemplate
from visualizer.templates.playback_template import PlaybackTemplate, PlaybackButtons
from visualizer.templates.game_frame import GameFrame

class Adapter:
    """
    The Adapter class can be considered the "Master Controller" of the Visualizer; it works in tandem with main.py.
    Main.py will call many of the methods that are provided in here to keep the Visualizer moving smoothly.
    """

    def __init__(self, screen):
        self.screen: pygame.Surface = screen
        self.bytesprites: list[ByteSprite] = []
        self.populate_bytesprite: pygame.sprite.Group = pygame.sprite.Group()
        self.menu: MenuTemplate = Basic(screen, 'Five Nights at The ACM')
        self.playback: PlaybackTemplate = PlaybackTemplate(screen)
        self.turn_number: int = 0
        self.turn_max: int = MAX_TICKS
        self.game_frame = GameFrame(self.screen)

    # Define any methods button may run

    def start_menu_event(self, event: pygame.event) -> Any:
        """
        This method is used to manage any events that will occur on the starting screen. For example, a start button
        is implemented currently. Pressing it or pressing enter will start the visualizer to show the game's results.
        This method will manage any specified events and return them (hence why the return type is Any). Refer to
        menu_templates.py's start_events method for more info.
        :param event: The pygame event triggered each frame. See
        `pygame <https://www.pygame.org/docs/ref/event.html for more information>`_
        for more information.
        :return: Any specified event desired in the start_events method
        """
        return self.menu.start_events(event)

    def start_menu_render(self) -> None:
        """
        Renders and shows everything in the start menu.
        :return: None
        """
        self.menu.start_render()

    def on_event(self, event) -> PlaybackButtons:
        """
        By giving this method an event, this method can execute whatever is specified. An example is provided below
        and commented out. Use as necessary.
        :param event: The pygame event triggered each frame. See
        `pygame <https://www.pygame.org/docs/ref/event.html for more information>`_
        for more information.
        :return: None
        """

        # The line below is an example of what this method could be used for.
        # self.button.mouse_clicked(event)
        return self.playback.playback_events(event)

    def prerender(self) -> None:
        """
        This will handle anything that needs to be completed before animations start every turn.
        :return: None
        """
        ...

    def continue_animation(self) -> None:
        """
        This method is used after the main.py continue_animation() method.
        :return: None
        """
        ...

    def recalc_animation(self, turn_log: dict) -> None:
        """
        This method is called every time the turn changes
        :param turn_log: A dictionary containing the entire turn state
        :return: None
        """
        self.turn_number = turn_log['tick']

    from visualizer.bytesprites.tileBS import TileBS

    def populate_bytesprite_factories(self) -> dict[int, Callable[[pygame.Surface], ByteSprite]]:
        """
        Instantiate all bytesprites for each objectType and add them here using the value of ObjectType as the key
        and the factory function as the value.
        """
        return {
            4: AvatarBS.create_bytesprite,
            7: TileBS.create_bytesprite,
            8: WallBS.create_bytesprite,
        }

    def render(self) -> None:
        """
        This method contains all logic for rendering additional text, buttons, and other visuals
        during the playback phase.
        :return: None
        """

        # Draw the game background as transparent black outside the frame
        frame_rect = self.game_frame.get_rect()
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))  # semi-transparent black
        overlay.fill((0, 0, 0, 0), frame_rect)  # clear out game area
        self.screen.blit(overlay, (0, 0))

        # Draw the border
        self.game_frame.render()

        # Draw the scoreboard above the border
        text = Text(self.screen, f'{self.turn_number} / {self.turn_max}', 32)
        text.rect.center = Vector(*frame_rect.midtop).add_y(20).as_tuple()
        text.render()

        # Draw playback buttons/UI
        self.playback.playback_render()


    def clean_up(self) -> None:
        """
        This method is called after rendering each frame.
        :return: None
        """
        ...

    def results_load(self, results: dict) -> None:
        """
        This method is called to load the end screen for the visualizer.
        :param results: A dictionary containing the results of the run
        :return: None
        """
        self.menu.load_results_screen(results)

    def results_event(self, event: pygame.event) -> Any:
        """
        This method is called to handle events of the visualizer in the end screen
        :param event: The pygame event triggered each frame. See
        `pygame <https://www.pygame.org/docs/ref/event.html>`_
        for more information.
        :return: Any value that is defined in the results_events
        """
        return self.menu.results_events(event)

    def results_render(self) -> None:
        """
        This renders the end screen for the visualizer
        :return:
        """
        self.menu.results_render()
