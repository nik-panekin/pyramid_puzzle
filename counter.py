"""Module for implementation the Counter class.
"""
import pygame

from static_text import StaticText

class Counter():
    """The Counter class implements visual incremental counter functionality.
    """
    def __init__(self, topleft: tuple, prefix_text: str, color: tuple,
                 font: pygame.font.Font):
        """Input:
            topleft - a tuple(x_left: int, y_top: int) for top-left corner
                of the Counter object;
            prefix_text - a text string preceding counter numeric value;
            color - tuple(r: int, g: int, b: int) for counter text color;
            font - pygame.font.Font object for drawing couter text.
        """
        self.topleft = topleft
        self.prefix_text = prefix_text
        self.color = color
        self.font = font
        self.reset()

    def reset(self):
        """Resets counter value to 0.
        """
        self.value = 0
        self._prepare_onscreen_text()

    def increment(self):
        """Increments counter value by 1.
        """
        self.value += 1
        self._prepare_onscreen_text()

    def draw(self):
        """Draws counter text representation.
        """
        self.onscreen_text.draw()

    # Prepares counter graphical representation for future drawing
    def _prepare_onscreen_text(self):
        self.onscreen_text = StaticText(self.prefix_text + str(self.value),
                                        self.color, self.font)
        self.onscreen_text.rect.topleft = self.topleft
