from game.utils.vector import Vector


class Config:
    """
    Configuration class for the game visualizer. By encapsulating the visualizer settings in a class, the readonly
    nature of the following settings are enforced to a greater degree.

    **Number Of Frames Per Turn**
        Number of frames per turn is an int representing the number of animation frames on
        each turn. See spritesheets for an example of what is needed for 4 frames per turn.
        Set this to 1 if you do not want any animations.

    -----

    **Tile Size**
        Tile size is an int that represents the size of each sprite (it's a square, so this
        applies to both width and height).

    -----

    **Scale**
        Scale is an int that represents the ratio between the tile size and the number of
        pixels that it will take on the visualizer itself.

    -----

    **Screen Size**
        Screen size is a Vector that represents the dimensions of the visualizer.

    -----

    **Frame Rate**
        Frame rate is an int that represents the number of frames per second.

    -----

    **Background Color**
        Background Color is a tuple of 3 ints representing the red, green, and blue values
        of the background.

    -----

    **Gameboard Margin Left**
        Gameboard Margin Left is an int representing the margin from the left side
        of the screen that the gameboard will adhere to.

    -----

    **Gameboard Margin Top**
        Gameboard Margin Top is an int representing the margin from the top side of
        the screen that the gameboard will adhere to.

    -----

    **Visualize Held Items**
        Visualize Held Items is a boolean that represents if held items should be
        rendered and has supporting ByteSprites.

    -----
    """

    __NUMBER_OF_FRAMES_PER_TURN: int = 4
    __TILE_SIZE: int = 32
    __SCALE: int = 1
    __SCREEN_SIZE: Vector = Vector(x=1280, y=720)  # width, height
    __FRAME_RATE: int = 12
    __BACKGROUND_COLOR: (int, int, int) = 0, 0, 0
    __GAME_BOARD_MARGIN_LEFT: int = 31
    __GAME_BOARD_MARGIN_TOP: int = 39
    __VISUALIZE_HELD_ITEMS: bool = False

    @property
    def NUMBER_OF_FRAMES_PER_TURN(self) -> int:
        """
        If you have an animation, this will be the number of frames the animation goes through for each turn.
        :return: int
        """
        return self.__NUMBER_OF_FRAMES_PER_TURN

    @property
    def TILE_SIZE(self) -> int:
        """
        This will be the size of the tile; it is a square.
        :return: int
        """
        return self.__TILE_SIZE

    @property
    def SCALE(self) -> int:
        """
        Scale is for the tile size being scaled larger.
        For example: With a 16x16 tile, it can be scaled by 4 to be a 64x64 tile on the visualizer.
        :return: int
        """
        return self.__SCALE

    @property
    def SCREEN_SIZE(self) -> Vector:
        """
        The screen size is the overall screen size.
        The x and y values of the Vector object returned represent the horizontal and vertical lengths
        of the screen respectively.
        :return: Vector
        """
        return self.__SCREEN_SIZE

    #
    @property
    def FRAME_RATE(self) -> int:
        """
        Frame Rate is the overall frames per second.
        :return: int
        """
        return self.__FRAME_RATE

    @property
    def BACKGROUND_COLOR(self) -> (int, int, int):
        """
        This is where you can set the default background color.
        :return: tuple of 3 ints representing the red, blue, and green values.
        """
        return self.__BACKGROUND_COLOR

    @property
    def GAME_BOARD_MARGIN_LEFT(self) -> int:
        """
        This is where you can set the left margin for the main game board.
        :return: int
        """
        return self.__GAME_BOARD_MARGIN_LEFT

    @property
    def GAME_BOARD_MARGIN_TOP(self) -> int:
        """
        This is where you can set the top margin for the main game board.
        :return: int
        """
        return self.__GAME_BOARD_MARGIN_TOP

    @property
    def VISUALIZE_HELD_ITEMS(self) -> bool:
        """
        This is where you can set if you want held items to be displayed in the visualizer.
        :return: bool
        """
        return self.__VISUALIZE_HELD_ITEMS
