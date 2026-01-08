from dataclasses import dataclass
from functools import reduce
from enum import Flag, auto

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from game.utils.vector import Vector
from visualizer.utils.button import Button, ButtonColors
from visualizer.utils.text import Text

"""
This file is for creating a default template for the playback implementation for the Visualizer. This will be displayed
while the game is running, with buttons including pause, speed up, slow down, restart, and save to mp4.
"""


class PlaybackButtons(Flag):
    """
    These are enums that are used to represent the playback buttons on the visualizer. They inherit from `Flag` and not
    `Enum` because Flag enums can use bitwise operators (& AND, | OR, ^ XOR, ~ INVERT). This allows for multiple values
    to be returned at the same time. Refer to https://docs.python.org/3.11/library/enum.html#enum.Flag to read more on
    it.
    """
    PAUSE_BUTTON = auto()
    SAVE_BUTTON = auto()
    NEXT_BUTTON = auto()
    PREV_BUTTON = auto()
    START_BUTTON = auto()
    END_BUTTON = auto()
    NORMAL_SPEED_BUTTON = auto()
    FAST_SPEED_BUTTON = auto()
    FASTEST_SPEED_BUTTON = auto()


class PlaybackTemplate:
    """
    This class provides a menu of buttons during runtime of the visualizer to control the playback
    of the visualizer, including pausing, start, end, frame scrubbing, speeding up, and slowing down, as well as
    saving it to a .mp4 file.

    Buttons from this template are centered at the bottom of the screen, placed in three rows of three.
    """

    def __init__(self, screen: pygame.Surface):
        buttoncolors = ButtonColors(
            fg_color="#ffffff",  # White text
            fg_color_hover="#ffff00",  # Yellow text on hover
            fg_color_clicked="#00ff00",  # Green text when clicked
            bg_color="#333399",  # Dark purple background
            bg_color_hover="#6666cc",  # Lighter purple on hover
            bg_color_clicked="#111166"  # Darker purple when clicked
        )
        BUTTON_SIZE = 25
        self.screen: pygame.Surface = screen
        self.pause_button: Button = Button(self.screen, 'Pause', lambda: PlaybackButtons.PAUSE_BUTTON, font_size=12, colors=buttoncolors)
        self.next_button: Button = Button(self.screen, 'Next', lambda: PlaybackButtons.NEXT_BUTTON, font_size=12, colors=buttoncolors)
        self.prev_button: Button = Button(self.screen, 'Prev', lambda: PlaybackButtons.PREV_BUTTON, font_size=12, colors=buttoncolors)
        self.start_button: Button = Button(self.screen, 'Start', lambda: PlaybackButtons.START_BUTTON, font_size=12, colors=buttoncolors)
        self.end_button: Button = Button(self.screen, 'End', lambda: PlaybackButtons.END_BUTTON, font_size=12, colors=buttoncolors)
        self.save_button: Button = Button(self.screen, 'Save', lambda: PlaybackButtons.SAVE_BUTTON, font_size=12, colors=buttoncolors)
        self.normal_speed_button: Button = Button(self.screen, '1x', lambda: PlaybackButtons.NORMAL_SPEED_BUTTON,
                                                  font_size=12, colors=buttoncolors)
        self.fast_speed_button: Button = Button(self.screen, '2x', lambda: PlaybackButtons.FAST_SPEED_BUTTON,
                                                font_size=12, colors=buttoncolors)
        self.fastest_speed_button: Button = Button(self.screen, '4x', lambda: PlaybackButtons.FASTEST_SPEED_BUTTON,
                                                   font_size=12, colors=buttoncolors)
        for btn in (
                self.pause_button, self.next_button, self.prev_button,
                self.start_button, self.end_button, self.save_button,
                self.normal_speed_button, self.fast_speed_button, self.fastest_speed_button
        ):
            self._resize_button(btn, BUTTON_SIZE)

        self.prev_button.rect.center = Vector(*self.screen.get_rect().center).add_x_y(150, 350).as_tuple()
        self.pause_button.rect.center = Vector(*self.screen.get_rect().center).add_x_y(-150, 350).as_tuple()
        self.next_button.rect.center = Vector(*self.screen.get_rect().center).add_x_y(100, 350).as_tuple()
        self.start_button.rect.center = Vector(*self.screen.get_rect().center).add_x_y(-200, 350).as_tuple()
        self.save_button.rect.center = Vector(*self.screen.get_rect().center).add_x_y(-100, 350).as_tuple()
        self.end_button.rect.center = Vector(*self.screen.get_rect().center).add_x_y(100, 350).as_tuple()
        self.normal_speed_button.rect.center = Vector(*self.screen.get_rect().center).add_x_y(-50, 350).as_tuple()
        self.fast_speed_button.rect.center = Vector(*self.screen.get_rect().center).add_y(350).as_tuple()
        self.fastest_speed_button.rect.center = Vector(*self.screen.get_rect().center).add_x_y(50, 350).as_tuple()


    def _resize_button(self, button: Button, size: int = 25) -> None:
        button.rect.width = size
        button.rect.height = size

    def playback_render(self) -> None:
        """
        This renders all the playback buttons.
        :return: None
        """
        self.prev_button.render()
        self.pause_button.render()
        self.next_button.render()
        self.start_button.render()
        self.save_button.render()
        self.end_button.render()
        self.normal_speed_button.render()
        self.fast_speed_button.render()
        self.fastest_speed_button.render()

    def playback_events(self, event: pygame.event) -> PlaybackButtons:
        """
        This handles all the playback events. By using the given event, this will return the playback buttons and
        execute each one's function. This is done by using the `reduce()` method. Read the documentation on the
        `reduce()` method for more information. Refer to the Button class for more information on how the
        mouse.clicked() method works.
        :param event:
        :return: PlaybackButtons
        """
        return reduce(lambda a, b: a | b,
                      (self.pause_button.mouse_clicked(event, default=PlaybackButtons(0)),
                       self.save_button.mouse_clicked(event, default=PlaybackButtons(0)),
                       self.next_button.mouse_clicked(event, default=PlaybackButtons(0)),
                       self.prev_button.mouse_clicked(event, default=PlaybackButtons(0)),
                       self.start_button.mouse_clicked(event, default=PlaybackButtons(0)),
                       self.end_button.mouse_clicked(event, default=PlaybackButtons(0)),
                       self.normal_speed_button.mouse_clicked(event, default=PlaybackButtons(0)),
                       self.fast_speed_button.mouse_clicked(event, default=PlaybackButtons(0)),
                       self.fastest_speed_button.mouse_clicked(event, default=PlaybackButtons(0))))
