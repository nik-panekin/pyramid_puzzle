"""Module for implementation the BlinkingRect class.
"""
import math

import pygame

from rounded_rect import RoundedRect

BLINKING_SPEED = 0.05 # Radians per frame
BRIGHTNESS_HIGH = 2.0 # High brightness factor (must be greater than 1.0)

class BlinkingRect(RoundedRect):
    """The BlinkingRect class adds blinking feature to the RoundedRect class.
    The bright ('blinking') color is auto-calculated.
    """
    def __init__(self, width: int, height: int, color: tuple):
        """The parameters are exactly the same as for RoundedRect constructor.
        """
        super().__init__(width, height, color)

        self.blinking = None

    def start_blinking(self):
        """Starts blinking animation.
        """
        self.blinking = 0

    def stop_blinking(self):
        """Stops blinking animation.
        """
        self.blinking = None

    def is_blinking(self):
        """Returns True if blinking is in progress. Otherwise - False.
        """
        return self.blinking != None

    def update(self):
        """Updates internal blinking parameter. Should be called every frame.
        """
        if self.blinking != None:
            self.blinking += BLINKING_SPEED
            if self.blinking >= math.pi:
                self.blinking -= math.pi

    def draw(self):
        """Draws blinking rounded rectangle.
        """
        if self.blinking != None:
            old_color, old_border_color = self.color, self.border_color
            self.color = [self._adjust_brightness(i) for i in old_color]
            self.border_color = [self._adjust_brightness(i)
                                 for i in old_border_color]
            super().draw()
            self.color, self.border_color = old_color, old_border_color
        else:
            super().draw()

    # Returns color component with brightness altered (for blinking effect)
    def _adjust_brightness(self, color: int) -> int:
        return min(int(color + color * (BRIGHTNESS_HIGH - 1)
                       * abs(math.sin(self.blinking))), 255)
