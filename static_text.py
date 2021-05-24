"""Module for implementation the StaticText class.
"""
import pygame

class StaticText():
    """The StaticText class instance stores pre-rendered text for quick
    blitting onto the screen surface.

    Public attributes:
        rect: pygame.Rect (read only) - stores bounding rectangle for rendered
            text image. Its properties can be modified for text on-screen
            positioning.
    """
    def __init__(self, text: str, color: tuple, font: pygame.font.Font):
        """Input:
            text - string value to render;
            color - tuple(r: int, g: int, b: int) representing text color;
            font - pygame.font.Font object for drawing text.
        """
        self.surf = font.render(text, True, color)
        self.rect = self.surf.get_rect()

    def draw(self):
        """Draws pre-rendered text.
        """
        ds = pygame.display.get_surface()
        ds.blit(self.surf, self.rect)
