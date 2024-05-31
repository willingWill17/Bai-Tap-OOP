import pygame
import constants as c 
from math import *

class Stick:
    """
    Class representing the stick used in the game.
    """

    def __init__(self,screen=None,game=None):
        """
        Initialize the stick object.
        """
        # self.game = Game()
        self.screen=screen
        self.x = 0
        self.y = 0
        self.angle = 0
        self.image = pygame.image.load('assets/stick.png')
        self.rect = self.image.get_rect()
        self.rect.center = (300, 300)
        self.original_image = self.image
        self.dist_to_ball = 180
        self.is_charging = False
        self.hit = False
        self.hit_force = 0
        self.remote_hit = False


    def set_angle(self, ball_obj, pos=(-100, -100), stick_movable=True):
        """
        Set the angle of the stick.
        
        Args:
            ball_obj (Ball): The ball object.
            pos (tuple): The position tuple. Default is (-100, -100).
            stick_movable (bool): Flag to control whether the stick can move.
        """
        if stick_movable:
            if pos[0] == -100:
                position = pygame.mouse.get_pos()
            else:
                position = pos
            self.x = position[0]
            self.y = position[1]
            self.angle = degrees(atan2(ball_obj.y - self.y, ball_obj.x - self.x))


    def draw(self, balls,stick_movable=True):
        """
        Draw the stick on the screen.
        
        Args:
            balls (list): List of balls on the screen.
            stick_movable (bool): Flag to control whether the stick can move.
        """
        if stick_movable:
            if self.is_charging:
                self.dist_to_ball += 0.5
                if self.dist_to_ball > 250:
                    self.dist_to_ball = 250
            else:
                self.dist_to_ball -= 8
                if self.dist_to_ball < 180:
                    self.dist_to_ball = 180
            if self.hit and self.dist_to_ball == 180:
                self.hit = False
                if not self.game.menu.is_hosting or self.game.turn == c.PLAYER1:
                    balls[0].set_force_angle(self.hit_force, self.angle)
                    self.game.after_hit = True
                if self.game.menu.is_connected and self.game.turn == c.PLAYER2:
                    self.remote_hit = True

            self.image = pygame.transform.rotate(self.original_image, -self.angle - 90)
            x, y = self.rect.center
            self.rect = self.image.get_rect()
            angle = self.angle
            self.x = balls[0].x - self.dist_to_ball * cos(radians(angle))
            self.y = balls[0].y - self.dist_to_ball * sin(radians(angle))
            self.rect.center = (int(self.x), int(self.y))
        
        self.screen.blit(self.image, self.rect)
