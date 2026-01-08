import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


class SpriteSheet:
    """
    The SpriteSheet class is a utility class to help load and dissect sprite sheets.
    It splits the sprite sheet into a list of rows and turns each row into a list of images.
    """

    def __init__(self, filename):
        """Load the sheet."""
        try:
            # Use convert_alpha() to preserve transparency
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle: tuple[int, int, int, int],
                 colorkey: pygame.Color | None = None) -> pygame.Surface:
        """
        Load a specific image from a specific location .
        :param rectangle: A tuple of ints representing x,y,width,height
            Where x is the distance from the left, y is the distance from the top, width is width of a single sprite
            frame, and height is the height of a single sprite frame.
        :param colorkey: The color to be made transparent on this image.
            pygame.Color(255,0,255) is recommended for this use. See the pygame
            `docs <https://www.pygame.org/docs/ref/color.html>`_
            for more details.
        :return: A Surface object with the loaded sprite. See the pygame
            `docs <https://www.pygame.org/docs/ref/surface.html>`_
            for more details.
        """
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)

        # Create a surface that supports per-pixel alpha
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)

        return image

    def images_at(self, rects: list[tuple[int, int, int, int]],
                  colorkey: pygame.Color | None = None) -> list[pygame.Surface]:
        """
        Load a bunch of images and return them as a list.
        :param rects: list of tuples containing the locations to load
        :param colorkey: The color to be made transparent on an image.
            pygame.Color(255,0,255) is recommended for this use. See the pygame
            `docs <https://www.pygame.org/docs/ref/color.html>`_
            for more details.
        :return: a list of Surfaces with the loaded images. See the pygame
            `docs <https://www.pygame.org/docs/ref/surface.html>`_
            for more details.
        """
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect: tuple[int, int, int, int], image_count: int,
                   colorkey: pygame.Color | None = None) -> list[pygame.Surface]:
        """
        Load a whole strip of images cut equally along the dimensions provided, and return them as a list.
        :param rect: A tuple of ints representing x,y,width,height.
            Where x is the distance from the left, y is the distance from the top, width is width of a single sprite
            frame, and height is the height of a single sprite frame.
        :param image_count: the number of images/sprite frames to load from a single row
        :param colorkey: The color to be made transparent on an image.
            pygame.Color(255,0,255) is recommended for this use. See the pygame
            `docs <https://www.pygame.org/docs/ref/color.html>`_
            for more details.
        :return: a list of Surfaces with the loaded images. See the pygame
            `docs <https://www.pygame.org/docs/ref/surface.html>`_
            for more details.
        """
        tups: list[tuple[int, int, int, int]] = [
            (rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
            for x in range(image_count)
        ]
        return self.images_at(tups, colorkey)
