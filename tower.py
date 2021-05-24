"""Module for implementation the Tower class.
"""
import pygame

from disk import Disk
from rounded_rect import RoundedRect

class Tower(RoundedRect):
    """The Tower class implements the basic rules of the pyramid puzzle. Also
    it handles drawing the rod.

    Public attributes:
        disks: list(Disk) (read only) - a list of Disks strung on the rod.
    """
    def __init__(self, width: int, height: int, color: tuple):
        """The parameters are exactly the same as for RoundedRect constructor.
        """
        super().__init__(width, height, color)

        self.disks = []

    def draw(self):
        """Drawing a rod.
        """
        ds = pygame.display.get_surface()

        outer_radius = int(self.rect.height / 2)
        pygame.draw.rect(ds, self.border_color, self.rect,
                         border_top_left_radius=outer_radius,
                         border_top_right_radius=outer_radius)

        inner_rect = self.get_inner_rect()
        inner_radius = int(inner_rect.height / 2)
        pygame.draw.rect(ds, self.color, inner_rect,
                         border_top_left_radius=inner_radius,
                         border_top_right_radius=inner_radius)

    def contains_point(self, point: tuple) -> bool:
        """Checks if a given point is inside the rod rectangle area or any
        Disk object belonging to the Tower instance.

        Input:
            point - a tuple(x: int, y: int) representing point to check.
        Returns:
            True - if the point is inside mentioned above areas;
            False - otherwise.
        """
        if super().contains_point(point):
            return True

        for disk in self.disks:
            if disk.contains_point(point):
                return True

        return False

    def can_put(self, disk: Disk) -> bool:
        """Checks if a given Disk object can be put on top of the Tower object.
        Only smaller by width disks are allowed.

        Input:
            disk - a Disk instance to check.
        Returns:
            True - if the Disk object can be put on top of the Tower object;
            False - otherwise.
        """
        if not self.disks:
            return True

        if self.disks[-1].rect.width < disk.rect.width or disk in self.disks:
            return False

        return True

    def put(self, disk: Disk) -> bool:
        """Puts (if possible) a given Disk object on top of the Tower object.

        Input:
            disk - a Disk instance to put.
        Returns:
            True - if the Disk object has been put on top of the Tower object;
            False - otherwise.
        """
        if not self.can_put(disk):
            return False

        disk.rect.midbottom = self.get_peak_point()
        self.disks.append(disk)

        return True

    def get(self) -> Disk:
        """Gets the topmost Disk object from the Tower object and removes it
        from inner list.

        Returns:
            Disk instance that has been got;
            None - if the Tower is empty.
        """
        if self.disks:
            return self.disks.pop()
        else:
            return None

    def peep(self) -> Disk:
        """Returns the topmost Disk object of the Tower object (not removing
        it from the list). Returns None if the Tower is empty.
        """
        if self.disks:
            return self.disks[-1]
        else:
            return None

    def get_peak_point(self) -> tuple:
        """Returns the highest point of the stack of Disk objects (not the rod
        height) in form of a tuple(x: int, y: int).
        """
        if self.disks:
            return self.disks[-1].rect.midtop
        else:
            return self.rect.midbottom
