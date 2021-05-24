"""Module for implementation the RoundedRect class.
"""
import pygame

# Brightness lowering for border color
# Must be in range (0..1) - not inclusively
BRIGHTNESS_LOW = 0.5
BORDER_WIDTH = 4 # Inner border width in pixels

class RoundedRect():
    """The RoundedRect class simplifies drawing filled rectangles with rounded
    corners and thick border. The color of border is auto-calculated.

    Public attributes:
        rect: pygame.Rect (read only) - stores rectangle datastructure for
            drawing. Its properties can be modified for positioning.
    """
    def __init__(self, width: int, height: int, color: tuple):
        """Input:
            width - integer value for rectangle width;
            height - integer value for rectangle height;
            color - tuple(r: int, g: int, b: int) for rectangle main color.
        """
        self.color = color
        self.border_color = [int(i * BRIGHTNESS_LOW) for i in self.color]
        self.rect = pygame.Rect(0, 0, width, height)

    def get_inner_rect(self) -> pygame.Rect:
        """Returns pygame.Rect instance representing inner rectangle filled
        with main color.
        """
        inner_rect = pygame.Rect(0, 0, self.rect.width - 2 * BORDER_WIDTH,
                                 self.rect.height - 2 * BORDER_WIDTH)
        inner_rect.center = self.rect.center
        return inner_rect

    def draw(self):
        """Draws rounded rectangle.
        """
        ds = pygame.display.get_surface()

        pygame.draw.rect(ds, self.border_color, self.rect,
                         border_radius=int(self.rect.height / 2))

        inner_rect = self.get_inner_rect()
        pygame.draw.rect(ds, self.color, inner_rect,
                         border_radius=int(inner_rect.height / 2))

    def contains_point(self, point: tuple) -> bool:
        """Checks if a given point is inside the RoundedRect object area.

        Input:
            point - a tuple(x: int, y: int) representing point to check.
        Returns:
            True - if the point is inside the rectangular area;
            False - otherwise.
        """
        return self.rect.collidepoint(point)
