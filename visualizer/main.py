import ast
import math
import sys
import os
import cv2
import game.config
from typing import Callable
from game.utils.vector import Vector
from visualizer.adapter import Adapter
from visualizer.bytesprites.bytesprite import ByteSprite
from visualizer.config import Config
from visualizer.utils.log_reader import logs_to_dict
from visualizer.templates.playback_template import PlaybackButtons
from threading import Thread

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


class ByteVisualiser:
    """
    The Byte Visualiser is a generic visualiser that uses `pygame <https://www.pygame.org/docs/>`_
    to visualise the game board using the 2-dimensional list of tiles and the occupied by and, optionally,
    the held_item attribute. It also calls the adapter class method to minimize the edits needed to this file.
    """

    def __init__(self, end_time: int = -1, skip_start: bool = False, playback_speed: float = 1.0,
                 fullscreen: bool = False, save_video: bool = False, loop_count: int = 1,
                 turn_start: int = 0, turn_end: int = -1, log_dir: str | None = None):
        """
        The constructor for the ByteVisualiser class
        :param end_time:
        :param skip_start:
        :param playback_speed:
        :param fullscreen:
        :param save_video:
        :param loop_count:
        :param turn_start:
        :param turn_end:
        :param log_dir:
        """
        pygame.init()
        self.logs = log_dir
        self.config: Config = Config()
        self.turn_logs: dict[str:dict] = {}
        self.size: Vector = self.config.SCREEN_SIZE
        self.tile_size: int = self.config.TILE_SIZE

        self.fullscreen: bool = fullscreen
        self.screen: pygame.Surface = pygame.display.set_mode(self.size.as_tuple(),
                                                              pygame.FULLSCREEN if self.fullscreen else pygame.SHOWN)
        self.adapter: Adapter = Adapter(self.screen)

        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.tick: int = turn_start * self.config.NUMBER_OF_FRAMES_PER_TURN
        self.turn_end: int = turn_end
        self.bytesprite_factories: dict[int: Callable[[pygame.Surface], ByteSprite]] = {}
        self.bytesprite_map: list[list[list[ByteSprite]]] = list()

        self.default_frame_rate: int = self.config.FRAME_RATE

        self.playback_speed: float = playback_speed
        self.paused: bool = False
        self.recording: bool = save_video

        # Scale for video saving (division can be adjusted, higher division = lower quality)
        self.scaled: tuple[int, int] = (self.size.x // 2, self.size.y // 2)

        self.end_time: int = end_time
        self.skip_start: bool = skip_start
        self.loop_count: int = loop_count

    @property
    def config(self) -> Config:
        """
        Property getter.
        :return: The Config file
        """
        return self.__config

    @config.setter
    def config(self, config: Config) -> None:
        """
        Property setter to enforce the type provided.
        :param config: A Config instance
        :return: None
        """
        if config is None or not isinstance(config, Config):
            # Error messaging should look like the message below going forward
            raise ValueError(
                f'{self.__class__.__name__}.config must be a Config. It is a(n) {type(config)} with the value of {config}')
        self.__config: Config = config

    @property
    def turn_logs(self) -> dict[str, dict]:
        """
        Property getter.
        :return: The turn logs of type dict[str, dict].
        """
        return self.__turn_logs

    @turn_logs.setter
    def turn_logs(self, turn_logs: dict[str, dict]) -> None:
        """
        Property setter to enforce the type provided.
        :param turn_logs: The turn logs of type dict[str, dict].
        :return: None
        """
        if turn_logs is None or not isinstance(turn_logs, dict):
            raise ValueError(f'{self.__class__.__name__}.turn_logs must be a dict. '
                             f'It is a(n) {type(turn_logs)} with the value of {turn_logs}')
        self.__turn_logs: dict = turn_logs

    @property
    def size(self) -> Vector:
        """
        Property getter
        :return: Vector class representing the size of the gameboard.
        """
        return self.__size

    @size.setter
    def size(self, size: Vector) -> None:
        """
        Property setter to enforce the type provided.
        :param size: Vector class representing the size of the gameboard.
        :return: None
        """
        if size is None or not isinstance(size, Vector):
            raise ValueError(
                f'{self.__class__.__name__}.size must be a Vector. It is a(n) {type(size)} with the value of {size}')
        self.__size: Vector = size

    @property
    def tile_size(self) -> int:
        """
        Property getter.
        :return: Tile Size is an int that represents the size of a tile in px. It is a square.
        """
        return self.__tile_size

    @tile_size.setter
    def tile_size(self, tile_size: int) -> None:
        """
        Property setter to enforce the type provided.
        :param tile_size: Tile Size is an int that represents the size of a tile in px. It is a square.
        :return: None
        """
        if tile_size is None or not isinstance(tile_size, int):
            raise ValueError(
                f'{self.__class__.__name__}.tile_size must be an int. It is a(n) {type(tile_size)} with the value of {tile_size}')
        self.__tile_size: int = tile_size

    @property
    def fullscreen(self) -> bool:
        """
        Property getter.
        :return: A bool representing if the fullscreen option should be enabled
        """
        return self.__fullscreen

    @fullscreen.setter
    def fullscreen(self, fullscreen: bool) -> None:
        """
        Property setter to enforce the type provided.
        :param fullscreen: A bool representing if the fullscreen option should be enabled
        :return: None
        """
        if fullscreen is None or not isinstance(fullscreen, bool):
            raise ValueError(
                f'{self.__class__.__name__}.fullscreen must be a bool. It is a(n) {type(fullscreen)} with the value of {fullscreen}')
        self.__fullscreen: bool = fullscreen

    @property
    def screen(self) -> pygame.Surface:
        """
        Property getter.
        :return: A pygame.Surface object representing the main window of the visualizer.
        """
        return self.__screen

    @screen.setter
    def screen(self, screen: pygame.Surface) -> None:
        """
        Property setter to enforce the type provided.
        :param screen: A pygame.Surface object representing the main window of the visualizer.
        :return: None
        """
        if screen is None or not isinstance(screen, pygame.Surface):
            raise ValueError(
                f'{self.__class__.__name__}.screen must be a pygame.Surface. It is a(n) {type(screen)} with the value of {screen}')
        self.__screen: pygame.Surface = screen

    @property
    def adapter(self) -> Adapter:
        """
        Property getter.
        :return: An instance of the Adapter class.
        """
        return self.__adapter

    @adapter.setter
    def adapter(self, adapter: Adapter) -> None:
        """
        Property setter to enforce the type provided.
        :param adapter: An instance of the Adapter class.
        :return: None
        """
        if adapter is None or not isinstance(adapter, Adapter):
            raise ValueError(
                f'{self.__class__.__name__}.adapter must be an Adapter. It is a(n) {type(adapter)} with the value of {adapter}')
        self.__adapter: Adapter = adapter

    @property
    def clock(self) -> pygame.time.Clock:
        """
        Property getter.
        :return: An instance of the `Clock <https://www.pygame.org/docs/ref/time.html#pygame.time.Clock>`_ class.
        """
        return self.__clock

    @clock.setter
    def clock(self, clock: pygame.time.Clock) -> None:
        """
        Property setter to enforce the type provided.
        :param clock: An instance of the `Clock <https://www.pygame.org/docs/ref/time.html#pygame.time.Clock>`_ class.
        :return: None
        """
        if clock is None or not isinstance(clock, pygame.time.Clock):
            raise ValueError(
                f'{self.__class__.__name__}.clock must be a pygame.time.Clock. It is a(n) {type(clock)} with the value of {clock}')
        self.__clock: pygame.time.Clock = clock

    @property
    def tick(self) -> int:
        """
        Property getter.
        :return: The number of frames the visualizer has gone through in the playback section, as an int.
        """
        return self.__tick

    @tick.setter
    def tick(self, tick: int) -> None:
        """
        Property setter to enforce the type provided.
        :param tick: The number of frames the visualizer has gone through in the playback section., as an int
        :return: None
        """
        if tick is None or not isinstance(tick, int):
            raise ValueError(
                f'{self.__class__.__name__}.tick must be an int. It is a(n) {type(tick)} with the value of {tick}')
        self.__tick: int = tick

    @property
    def turn_end(self) -> int:
        """
        Property getter.
        :return: The turn, as an int, to end the playback on.
        """
        return self.__turn_end

    @turn_end.setter
    def turn_end(self, turn_end: int) -> None:
        """
        Property setter to enforce the type provided.
        :param turn_end: The turn, as an int, to end the playback on.
        :return: None
        """
        if turn_end is None or not isinstance(turn_end, int):
            raise ValueError(
                f'{self.__class__.__name__}.turn_end must be an int. It is a(n) {type(turn_end)} with the value of {turn_end}')
        self.__turn_end: int = turn_end

    @property
    def bytesprite_factories(self) -> dict[int: Callable[[pygame.Surface], ByteSprite]]:
        """
        Property getter.
        :return: A dictionary with the int representation of the target ObjectType as the key and
            the ByteSprite factory child classes' create method as the value.
        """
        return self.__bytesprite_factories

    @bytesprite_factories.setter
    def bytesprite_factories(self, bytesprite_factories: dict) -> None:
        """
        Property setter to enforce the type provided.
        :param bytesprite_factories: A dictionary with the int representation of the target ObjectType as the key
            and the ByteSprite factory child classes' create method as the value.
        :return: None
        """
        if bytesprite_factories is None or not isinstance(bytesprite_factories, dict):
            raise ValueError(f'{self.__class__.__name__}.bytesprite_factories must be a dict. It is a(n) '
                             f'{type(bytesprite_factories)} with the value of {bytesprite_factories}')
        self.__bytesprite_factories: dict = bytesprite_factories

    @property
    def bytesprite_map(self) -> list[list[list[ByteSprite]]]:
        """
        Property getter.
        :return: A list[list[list[ByteSprite]]] containing the rows, columns, and layers of the ByteSprites to
            be rendered each frame of the playback phase.
        """
        return self.__bytesprite_map

    @bytesprite_map.setter
    def bytesprite_map(self, bytesprite_map: list[list[list[ByteSprite]]]) -> None:
        """
        Property setter to enforce the type provided.
        :param bytesprite_map: A list[list[list[ByteSprite]]] containing the rows, columns, and layers of the
            ByteSprites to be rendered each frame of the playback phase.
        :return: None
        """
        if bytesprite_map is None or not isinstance(bytesprite_map, list):
            raise ValueError(
                f'{self.__class__.__name__}.bytesprite_map must be a list. It is a(n) {type(bytesprite_map)} with the value of {bytesprite_map}')
        self.__bytesprite_map: list = bytesprite_map

    @property
    def default_frame_rate(self) -> int:
        """
        Property getter.
        :return: The default frame rate of the visualizer as an int.
        """
        return self.__default_frame_rate

    @default_frame_rate.setter
    def default_frame_rate(self, default_frame_rate: int) -> None:
        """
        Property setter to enforce the type provided.
        :param default_frame_rate: The default frame rate of the visualizer as an int.
        :return: None
        """
        if default_frame_rate is None or not isinstance(default_frame_rate, int):
            raise ValueError(
                f'{self.__class__.__name__}.default_frame_rate must be an int. It is a(n) {type(default_frame_rate)} with the value of {default_frame_rate}')
        self.__default_frame_rate: int = default_frame_rate

    @property
    def playback_speed(self) -> float:
        """
        Property getter.
        :return: The scale to apply to the default frame rate of the visualizer as a float.
        """
        return self.__playback_speed

    @playback_speed.setter
    def playback_speed(self, playback_speed: float) -> None:
        """
        Property setter to enforce the type provided.
        :param playback_speed: The scale to apply to the default frame rate of the visualizer as a float.
        :return: None
        """
        if playback_speed is None or not isinstance(playback_speed, float) or playback_speed < 1:
            raise ValueError(
                f'{self.__class__.__name__}.playback_speed must be a float greater than or equal to 1.0. It is a(n) {type(playback_speed)} with the value of {playback_speed}.')
        self.__playback_speed: float = playback_speed

    @property
    def paused(self) -> bool:
        """
        Property getter.
        :return: A bool representing if playback is paused or not.
        """
        return self.__paused

    @paused.setter
    def paused(self, paused: bool) -> None:
        """
        Property setter to enforce the type provided.
        :param paused: A bool representing if playback is paused or not.
        :return: None
        """
        if paused is None or not isinstance(paused, bool):
            raise ValueError(
                f'{self.__class__.__name__}.paused must be a bool. It is a(n) {type(paused)} with the value of {paused}')
        self.__paused: bool = paused

    @property
    def recording(self) -> bool:
        """
        Property getter.
        :return: A bool representing if playback is being recorded.
        """
        return self.__recording

    @recording.setter
    def recording(self, recording: bool) -> None:
        """
        Property setter to enforce the type provided.
        :param recording: A bool representing if playback is being recorded.
        :return: None
        """
        if recording is None or not isinstance(recording, bool):
            raise ValueError(
                f'{self.__class__.__name__}.recording must be a bool. It is a(n) {type(recording)} with the value of {recording}')
        self.__recording: bool = recording

    @property
    def scaled(self) -> tuple[int, int]:
        """
        Property getter.
        :return: A tuple of two ints representing the size of the saved video.
        """
        return self.__scaled

    @scaled.setter
    def scaled(self, scaled: tuple[int, int]) -> None:
        """
        Property setter to enforce the type provided.
        :param scaled: A tuple of two ints representing the size of the saved video.
        :return: None
        """
        if scaled is None or not isinstance(scaled, tuple) or len(scaled) != 2 or any(
                map(lambda x: not isinstance(x, int), scaled)):
            raise ValueError(
                f'{self.__class__.__name__}.scaled must be a tuple[int, int]. It is a(n) {type(scaled)} with the value of {scaled}')
        self.__scaled: tuple[int, int] = scaled

    @property
    def writer(self) -> cv2.VideoWriter:
        """
        Property getter.
        :return: A cv2.VideoWriter to write the video to an output file.
        """
        return self.__writer

    @writer.setter
    def writer(self, writer: cv2.VideoWriter) -> None:
        """
        Property setter to enforce the type provided.
        :param writer: A cv2.VideoWriter to write the video to an output file.
        :return: None
        """
        if writer is None or not isinstance(writer, cv2.VideoWriter):
            raise ValueError(
                f'{self.__class__.__name__}.writer must be an cv2.VideoWriter. It is a(n) {type(writer)} with the value of {writer}')
        self.__writer: cv2.VideoWriter = writer

    @property
    def end_time(self) -> int:
        """
        Property getter
        :return: The amount of seconds, as an int, to wait on the results phase of the visualizer.
        """
        return self.__end_time

    @end_time.setter
    def end_time(self, end_time: int) -> None:
        """
        Property setter to enforce the type provided.
        :param end_time: The amount of seconds, as an int, to wait on the results phase of the visualizer.
        :return: None
        """
        if end_time is None or not isinstance(end_time, int):
            raise ValueError(
                f'{self.__class__.__name__}.end_time must be an int. It is a(n) {type(end_time)} with the value of {end_time}')
        self.__end_time: int = end_time

    @property
    def skip_start(self) -> bool:
        """
        Property getter.
        :return: A bool representing whether the starting screen should be skipped.
        """
        return self.__skip_start

    @skip_start.setter
    def skip_start(self, skip_start: bool) -> None:
        """
        Property setter to enforce the type provided.
        :param skip_start: A bool representing whether the starting screen should be skipped.
        :return: None
        """
        if skip_start is None or not isinstance(skip_start, bool):
            raise ValueError(
                f'{self.__class__.__name__}.skip_start must be a bool. It is a(n) {type(skip_start)} with the value of {skip_start}')
        self.__skip_start: bool = skip_start

    @property
    def loop_count(self) -> int:
        """
        Property getter.
        :return: The amount of times the visualizer should repeat the same game as an int.
        """
        return self.__loop_count

    @loop_count.setter
    def loop_count(self, loop_count: int) -> None:
        """
        Property setter to enforce the type provided.
        :param loop_count: The amount of times the visualizer should repeat the same game as an int.
        :return: None
        """
        if loop_count is None or not isinstance(loop_count, int):
            raise ValueError(
                f'{self.__class__.__name__}.loop_count must be an int. It is a(n) {type(loop_count)} with the value of {loop_count}')
        self.__loop_count: int = loop_count

    def load(self) -> None:
        """
        Loads the ByteSprite factories by calling the adapter and loads the logs as a dictionary
        :return: None
        """

        # if first turn log doens't exist, this can cause problems; can find better way to fix this
        self.turn_logs: dict = logs_to_dict(self.logs)
        self.bytesprite_factories = self.adapter.populate_bytesprite_factories()
        map_size: dict = self.turn_logs['turn_0001']['game_board']['map_size']

        # bytesprite_factories[7] is indexing to access the Tile object type
        self.bytesprite_map = [[[self.bytesprite_factories[7](self.screen), ]
                                for _ in range(map_size['x'])]
                               for _ in range(map_size['y'])]

    def prerender(self) -> None:
        """
        Fills the screen with the background color and calls the prerender method in the adapter class.
        :return: None
        """
        self.screen.fill(self.config.BACKGROUND_COLOR)
        self.adapter.prerender()

    def render(self, button_pressed: PlaybackButtons) -> bool:
        """
        Render every frame in the playback loop, the main loop of the visualizer.
        :param button_pressed: The bitflag enum of the buttons pressed during playback.
        :return: bool indicating whether the playback loop was successful or can't find the next turn.
        """
        # Run playback buttons method
        self.__playback_controls(button_pressed)

        # This renders all static images and templates from the adapter file before the game, placing it behind the game
        self.adapter.render()

        if self.tick % self.config.NUMBER_OF_FRAMES_PER_TURN == 0:
            # NEXT TURN
            turn: int = self.tick // self.config.NUMBER_OF_FRAMES_PER_TURN + 1
            if self.turn_logs.get(f'turn_{turn:04d}') is None or \
                    (self.turn_end != -1 and turn == self.turn_end):
                return False
            self.recalc_animation(self.turn_logs[f'turn_{turn:04d}'])
            self.adapter.recalc_animation(
                self.turn_logs[f'turn_{turn:04d}'])
        else:
            # NEXT ANIMATION FRAME
            self.continue_animation()
            self.adapter.continue_animation()

        pygame.display.flip()

        # If recording, save frames into video
        if self.recording:
            self.save_video()
            # Reduce ticks to just one frame per turn for saving video (can be adjusted)
            self.tick += self.config.NUMBER_OF_FRAMES_PER_TURN - 1
        self.tick += 1
        return True

    def __playback_controls(self, button_pressed: PlaybackButtons) -> None:
        """
        Method to deal with playback_controls in visualizer ran in render method.
        :param button_pressed: The bitflag enum of the buttons pressed during playback.
        :return: None
        """
        # If recording, do not allow the buttons to work
        if not self.recording:
            # Save button
            if PlaybackButtons.SAVE_BUTTON in button_pressed:
                self.writer: cv2.VideoWriter = cv2.VideoWriter("out.mp4", cv2.VideoWriter_fourcc(*'mp4v'),
                                                               self.default_frame_rate, self.scaled)
                self.recording = True
                self.playback_speed = 10.0
                self.tick = 0

            if self.tick % self.config.NUMBER_OF_FRAMES_PER_TURN == 0 and self.paused:
                self.tick = max(self.tick - self.config.NUMBER_OF_FRAMES_PER_TURN, 0)
            # Prev button to go back a frame
            if PlaybackButtons.PREV_BUTTON in button_pressed:
                turn = self.tick // self.config.NUMBER_OF_FRAMES_PER_TURN
                self.tick = (turn - 1) * self.config.NUMBER_OF_FRAMES_PER_TURN
            # Next button to go forward a frame
            if PlaybackButtons.NEXT_BUTTON in button_pressed:
                turn = self.tick // self.config.NUMBER_OF_FRAMES_PER_TURN
                self.tick = (turn + 1) * self.config.NUMBER_OF_FRAMES_PER_TURN
            # Start button to restart visualizer
            if PlaybackButtons.START_BUTTON in button_pressed:
                self.tick = 0
            # End button to end visualizer
            if PlaybackButtons.END_BUTTON in button_pressed:
                self.tick = self.config.NUMBER_OF_FRAMES_PER_TURN * (game.config.MAX_TICKS + 1)
            # Pause button to pause visualizer (allow looping of turn animation)
            if PlaybackButtons.PAUSE_BUTTON in button_pressed:
                self.paused = not self.paused
            if PlaybackButtons.NORMAL_SPEED_BUTTON in button_pressed:
                self.playback_speed = 1.0
            if PlaybackButtons.FAST_SPEED_BUTTON in button_pressed:
                self.playback_speed = 2.0
            if PlaybackButtons.FASTEST_SPEED_BUTTON in button_pressed:
                self.playback_speed = 4.0

    def save_video(self) -> None:
        """
        Method to deal with saving game to mp4 (called in render if save button pressed)
        :return: None
        """
        # Convert to PIL Image
        new_image = pygame.surfarray.pixels3d(self.screen.copy())
        # Rotate ndarray
        new_image = new_image.swapaxes(1, 0)
        # shrink size for recording
        new_image = cv2.resize(new_image, self.scaled)
        # Convert to OpenCV Image with numpy
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGR)
        # Write image and go to next turn
        self.writer.write(new_image)

    def recalc_animation(self, turn_data: dict) -> None:
        """
        Determine what bytesprites are needed at which location and calls logic to determine active spritesheet and
        render.
        :param turn_data: A dictionary of all the turn data for current turn
        :return: None
        """

        # Update tiles
        [tile[0].update(dict(), 0, Vector(y=y, x=x)) for y, row
         in enumerate(self.bytesprite_map) for x, tile
         in enumerate(row)]

        game_map: [[dict]] = turn_data['game_board']['game_map']
        for vec, go_container in game_map.items():
            # get the vectors from the json (they were stored as strings, so ast.literal_eval is necessary)
            vec: dict = ast.literal_eval(vec)

            # get the sublist from the current game object container
            objs: [dict] = go_container['sublist']

            # create bytesprites using the vector coordinates given
            # z is used for the current layer of making the bytesprite (i.e., if iteration = 5, currently on 5th layer)
            [self.__create_bytesprite(x=vec['x'], y=vec['y'], z=z, temp_tile=obj) for z, obj in
             enumerate(objs, start=1)]
            self.__clean_up_layers(x=vec['x'], y=vec['y'], z=len(objs) + 1)
            self.__clean_up_map(turn_data['game_board']['game_map'])

    def __clean_up_map(self, vecs: list[str]) -> None:
        def process_and_hash_vec_string(vec: str) -> int:
            vec_dict: dict[str, int] = ast.literal_eval(vec)
            return vec_dict['x'] * 17 + vec_dict['y'] * 19

        # using hashing to search by O(1) instead of O(n)
        hashed_vecs: set[int] = [process_and_hash_vec_string(vec) for vec in vecs]

        def is_used(x: int, y: int) -> bool:
            """
            Nested method to help make the logic more readable later.
            """
            return (x * 17 + y * 19) in hashed_vecs

        # clean up the layers on any coordinate as long as it was not used
        [self.__clean_up_layers(x=x, y=y, z=1) for y, row in enumerate(self.bytesprite_map)
         for x, _ in enumerate(row) if not is_used(x, y)]

    def __add_needed_layers(self, x: int, y: int, z: int) -> None:
        """
        Add layers ran in recalc_animation method.
        :param x: The column value of the calculation.
        :param y: The row value of the calculation.
        :param z: The layer value of the calculation.
        :return: None
        """
        if len(self.bytesprite_map[y][x]) < z + 1:
            self.bytesprite_map[y][x].append(None)

    def __create_bytesprite(self, x: int, y: int, z: int, temp_tile: dict | None) -> None:
        """
        Create a ByteSprite at current tile ran in recalc_animation method.
        :param x: The column value of the calculation.
        :param y: The row value of the calculation.
        :param z: The layer value of the calculation.
        :param temp_tile: Current tile in the recalc_animation method.
        :return: None
        """
        self.__add_needed_layers(x, y, z)
        if self.bytesprite_map[y][x][z] is None or \
                self.bytesprite_map[y][x][z].object_type != temp_tile['object_type']:
            if len(self.bytesprite_factories) == 0:
                raise ValueError(f'No ByteSprite factories have been provided for visualization!')
            # Check that a bytesprite template exists for current object type
            factory_function: Callable[[pygame.Surface], ByteSprite] | None = self.bytesprite_factories.get(
                temp_tile['object_type'])
            if factory_function is None:
                raise ValueError(
                    f'Must provide a bytesprite for each object type! Missing object_type: {temp_tile["object_type"]}')

            # Instantiate a new bytesprite on current layer
            self.bytesprite_map[y][x][z] = factory_function(self.screen)

        self.bytesprite_map[y][x][z].update(temp_tile, z, Vector(x=x, y=y))

    def __clean_up_layers(self, x: int, y: int, z: int) -> None:
        """
        Layer clean up method ran in recalc_animation method if the number of layers has decreased.
        :param x: The column value of the calculation.
        :param y: The row value of the calculation.
        :param z: The layer value of the calculation.
        :return: None
        """
        while len(self.bytesprite_map[y][x]) > z:
            self.bytesprite_map[y][x].pop()

    def continue_animation(self) -> None:
        """
        Continue the animation between each turn increment.
        :return: None
        """
        row: list
        tile: list
        sprite: ByteSprite
        [sprite.set_image_and_render() for row in self.bytesprite_map for tile in row for sprite in tile]

    def postrender(self) -> None:
        """
        Called after the render method in playback. This method calls the clean up method in the adapter and enforces
        the frames per second.
        :return:
        """
        self.adapter.clean_up()
        self.clock.tick(self.default_frame_rate * self.playback_speed)

    def loop(self) -> None:
        """
        The main loop for the visualizer. This method triggers the different phases.
        :return: None
        """
        for _ in range(self.loop_count):
            thread: Thread = Thread(target=self.load)
            thread.start()

            # Start Menu loop
            if not self.skip_start:
                self.__start_menu_loop()

            thread.join()

            # Playback Menu loop
            self.__play_back_menu_loop()

            # Results
            self.__results_loop()

        if self.recording:
            self.writer.release()

        sys.exit()

    #
    def __start_menu_loop(self) -> None:
        """
        Start menu phase of the visualizer. This method calls the start menu render and event methods in the adapter.
        :return: None
        """
        in_phase: bool = True
        while in_phase:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: sys.exit()
                    if event.key == pygame.K_RETURN: in_phase = False

                if in_phase:
                    in_phase = self.adapter.start_menu_event(event)

            self.adapter.start_menu_render()

            pygame.display.flip()
            self.clock.tick(self.default_frame_rate * self.playback_speed)

    def __play_back_menu_loop(self) -> None:
        """
        Playback phase of the visualizer. This method calls the pre, post, render, and event methods in the adapter.
        :return: None
        """
        in_phase: bool = True

        while in_phase:
            playback_buttons: PlaybackButtons = PlaybackButtons(0)
            # pygame events used to exit the loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: sys.exit()
                    if event.key == pygame.K_RETURN: in_phase = False

                playback_buttons = self.adapter.on_event(event)

            self.prerender()

            if in_phase:
                in_phase = self.render(playback_buttons)

            self.postrender()

    def __results_loop(self) -> None:
        """
        Results phase of the visualizer. This method calls the results render and event methods in the adapter.
        :return: None
        """
        in_phase: bool = True
        self.adapter.results_load(self.turn_logs['results'])
        ticks: int = 0
        while in_phase:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: sys.exit()
                    if event.key == pygame.K_RETURN: in_phase = False

                if in_phase:
                    in_phase = self.adapter.results_event(event)

            self.adapter.results_render()

            pygame.display.flip()

            if self.recording:
                self.save_video()

            if (self.end_time != -1 and ticks >= self.end_time * math.floor(
                    self.default_frame_rate * self.playback_speed)):
                break
            self.clock.tick(math.floor(self.default_frame_rate * self.playback_speed))
            ticks += 1


if __name__ == '__main__':
    byte_visualiser: ByteVisualiser = ByteVisualiser()
    byte_visualiser.loop()
