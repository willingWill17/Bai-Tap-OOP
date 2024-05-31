import pygame
import constants as c
font = pygame.font.Font('freesansbold.ttf', 10)
font_medium = pygame.font.Font('freesansbold.ttf', 16)

class Label:
    def __init__(self, x, y, text=""):
        """
        Initialize a Label object.

        Args:
            x (int): The x-coordinate of the label.
            y (int): The y-coordinate of the label.
            text (str): The text to display in the label.
        """
        self.x = x
        self.y = y
        self.text = text
        
    def draw(self, surface, text): 
        """
        Draw the label on the specified surface.

        Args:
            surface: The surface on which to draw the label.
            text (str): The text to display in the label.
        """
        tmp = font_medium.render(text, True, c.BLACK)     
        surface.blit(tmp, (self.x, self.y))
