import pygame
from constants import pos
from create import Create
class Cue(Create):
    """
    Represents the pool cue and its actions.
    """
    def __init__(self,pos):
        """
        Initializes the cue with a position.

        Parameters:
            pos (tuple): The initial position of the cue.
        """
        self.original_image = pygame.image.load("Assets/images/cue.png").convert_alpha()
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self, angle):
        """
        Updates the angle of the cue.

        Parameters:
            angle (float): The new angle of the cue.
        """
        self.angle = angle

    def draw(self, surface):
        """
        Draws the cue on the given surface.

        Parameters:
            surface (pygame.Surface): The surface to draw the cue on.
        """
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image,
                     (self.rect.centerx - self.image.get_width() / 2,
                      self.rect.centery - self.image.get_height() / 2))
