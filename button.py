"""Module for implementation the Button class.
"""
import pygame

from blinking_rect import BlinkingRect

class Button(BlinkingRect):
    """The Button class implements visual rectangular element with a text
    inside. It can be used for GUI.

    Public attributes:
        caption: str (read only) - stores button caption as an identifier.
    """
    def __init__(self, width: int, height: int, color: tuple, text: str,
                 text_color: tuple, font: pygame.font.Font):
        """Input:
            width, height, color are the same as for RoundedRect constructor;
            text - string value for button caption;
            text_color - tuple(r: int, g: int, b: int) for button caption
                color representation;
            font - pygame.font.Font object for drawing text caption.
        """
        super().__init__(width, height, color)

        self.caption = text
        self.text_surf = font.render(text, True, text_color)
        self.text_rect = self.text_surf.get_rect()

    def draw(self):
        """Draws the button.
        """
        super().draw()
        ds = pygame.display.get_surface()
        self.text_rect.center = self.rect.center
        ds.blit(self.text_surf, self.text_rect)
