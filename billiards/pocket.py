import pygame
import constants as c
class Pocket():
    """
    Class representing a pocket on the table.
    """

    def __init__(self, x, y, r=16):
        """
        Initialize a pocket.
        
        Args:
            x (int): x-coordinate of the pocket.
            y (int): y-coordinate of the pocket.
            r (int): Radius of the pocket.

        """
        self.x = x
        self.y = y
        self.color = c.WHITE
        self.radius = r

    def draw(self):
        pass