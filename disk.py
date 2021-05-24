"""Module for implementation the Disk class.
"""
import math

import pygame

from blinking_rect import BlinkingRect

MOVING_SPEED = 10 # Disk animation moving speed: pixels per frame

# Constants for disk animation phases
MOVING_PHASE_STARTING = 0
MOVING_PHASE_FLYING = 1
MOVING_PHASE_LANDING = 2

class Disk(BlinkingRect):
    """The main purpose of the Disk class is to implement smooth animation for
    moving a disk object from one rod to another.
    """
    def __init__(self, width: int, height: int, color: tuple):
        """The parameters are exactly the same as for RoundedRect constructor.
        """
        super().__init__(width, height, color)

        self.moving_phase = None
        self.start_point = (None, None)
        self.land_point = (None, None)
        self.fly_point = (None, None)
        self.delta = None
        self.angle = None

    def move(self, start_point: tuple, land_point: tuple, fly_point: tuple):
        """Initializes moving animation (should be called once per full cycle).

        Input:
            start_point - a tuple(x: int, y: int) for starting middle-bottom
                point of the Disk object;
            land_point - a tuple(x: int, y: int) for landing middle-bottom
                point of the Disk object;
            fly_point - a tuple(x: int, y: int) for middle-bottom point
                of the Disk object where it starts curvilinear motion.
        """
        self.rect.midbottom = start_point
        self.start_point = start_point
        self.land_point = land_point
        self.fly_point = fly_point
        self.angle = 0
        self.moving_phase = MOVING_PHASE_STARTING

    def is_moving(self) -> bool:
        """Returns True if the animation is in progress and False otherwise.
        """
        return self.moving_phase != None

    def update(self):
        """Updates coordinates of the Disk object while the animation is in
        progress. Should be called every frame.
        """
        super().update()

        if self.moving_phase == MOVING_PHASE_STARTING:
            self.rect.y -= MOVING_SPEED

            if self.rect.bottom <= self.fly_point[1]:
                self.rect.midbottom = self.fly_point
                self.delta = 2 * MOVING_SPEED / (self.start_point[0]
                                                 - self.land_point[0])
                self.angle = 0 if self.delta > 0 else math.pi
                self.moving_phase = MOVING_PHASE_FLYING

        elif self.moving_phase == MOVING_PHASE_FLYING:
            self.angle += self.delta
            radius = abs(self.start_point[0] - self.land_point[0]) / 2
            x0 = (self.start_point[0] + self.land_point[0]) / 2
            y0 = self.fly_point[1]
            self.rect.centerx = radius * math.cos(self.angle) + x0
            self.rect.bottom = y0 - radius * math.sin(self.angle) / 2

            if ((self.delta > 0 and self.angle >= math.pi)
                    or (self.delta < 0 and self.angle <= 0)):
                self.rect.centerx = self.land_point[0]
                self.rect.bottom = self.fly_point[1]
                self.moving_phase = MOVING_PHASE_LANDING

        elif self.moving_phase == MOVING_PHASE_LANDING:
            self.rect.y += MOVING_SPEED
            if self.rect.bottom >= self.land_point[1]:
                self.rect.midbottom = self.land_point
                self.moving_phase = None
