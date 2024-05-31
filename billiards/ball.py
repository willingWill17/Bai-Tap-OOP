import pygame
import constants as c
from math import cos, sin, radians

class Ball:
    """
    Class representing a ball object in the game.
    """

    def __init__(self,screen, pos=(50, 50), number=0):
        """
        Initialize a ball object.
        
        Args:
            pos (tuple): Initial position of the ball.
            number (int): Number associated with the ball.

        """
        self.screen=screen
        self.x = pos[0]
        self.y = pos[1]
        self.friction = 0.01 
        self.velocity = 0.0
        self.angle = 0
        self.radius = 10
        self.color = c.WHITE
        self.number = number

    def set_force_angle(self, force, angle):
        """
        Set the force and angle of the ball.
        
        Args:
            force (float): Magnitude of the force.
            angle (float): Angle of the force.

        """
        self.velocity = force
        self.angle = angle

    def draw(self):
        """
        Draw the ball on the screen.
        """
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.gfxdraw.filled_circle(self.screen, int(self.x), int(self.y), self.radius, self.color)
        pygame.gfxdraw.aacircle(self.screen, int(self.x), int(self.y), self.radius, self.color)
        text = font.render(str(self.number), True, c.WHITE)
        xoff = 5
        yoff = 4
        if self.number < 10:
            xoff = 2
        if self.number != 0:
            self.screen.blit(text, (int(self.x) - xoff, int(self.y) - yoff))

    def move(self):
        """
        Move the ball according to its velocity and angle.
        """
        self.x = self.x + self.velocity*cos(radians(self.angle))
        self.y = self.y + self.velocity*sin(radians(self.angle))
        ignore = True if (self.x == -200 and self.y == -200) else False
        if self.x > (c.WIDTH - c.MARGIN_RIGHT) - self.radius:
            self.x = (c.WIDTH - c.MARGIN_RIGHT) - self.radius
            self.angle = 180 - self.angle
        if self.x < self.radius + c.MARGIN_LEFT and not ignore:
            self.x = self.radius + c.MARGIN_LEFT
            self.angle = 180 - self.angle
        if self.y > c.HEIGHT - c.MARGIN_BOTTOM - self.radius - c.MENU_HEIGHT:
            self.y = c.HEIGHT - c.MARGIN_BOTTOM - self.radius - c.MENU_HEIGHT
            self.angle = 360 - self.angle
        if self.y < self.radius + c.MARGIN_TOP and not ignore:
            self.y = self.radius + c.MARGIN_TOP
            self.angle = 360 - self.angle

        self.velocity -= self.friction
        if self.velocity < 0:
            self.velocity = 0

    def draw_after_pocket(self, x, y):
        """
        Draw the ball after it has been pocketed.
        
        Args:
            x (int): x-coordinate of the ball.
            y (int): y-coordinate of the ball.

        """
        

        self.x = x
        self.y = y
        pygame.gfxdraw.filled_circle(self.screen, int(self.x), int(self.y), self.radius, self.color)
        pygame.gfxdraw.aacircle(self.screen, int(self.x), int(self.y), self.radius, self.color)
        text = font.render(str(self.number), True, c.WHITE)
        xoff = 5
        yoff = 4
        if self.number < 10:
            xoff = 2
        if self.number != 0:
            self.screen.blit(text, (int(self.x) - xoff, int(self.y) - yoff))
