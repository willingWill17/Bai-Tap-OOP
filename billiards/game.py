import pygame
from ball import Ball
from pocket import Pocket
from stick import Stick
from menu import Menu
import constants as c
from math import cos, sin, radians, atan2, degrees
from random import randint
import sys
from cmath import polar
from main import ball_collided, calc_distance,fix_overlap
hit_sound1 = pygame.mixer.Sound(r"assets/hit1.wav")
hit_sound2 = pygame.mixer.Sound(r"assets/hit2.wav")
hit_sound3 = pygame.mixer.Sound(r"assets/hit3.wav")
pocket_sound = pygame.mixer.Sound(r"assets/pocket.wav")
hit_cue_sound = pygame.mixer.Sound(r"assets/hit_cue.wav")
hit_wall_sound = pygame.mixer.Sound(r"assets/wall_hit.wav")
victory_sound = pygame.mixer.Sound(r"assets/victory.wav")

class Game:
    """
    Class representing the game state.
    """

    def __init__(self,screen,font_medium):
        """
        Initialize the game state.
        """
        self.font_medium=font_medium
        self.screen=screen
        self.balls = []
        self.balls_pocket_even = []
        self.balls_pocket_odd = []
        self.balls.append(Ball(screen,(600, 220)))
        for x in range(15):
            self.balls.append(Ball(screen,c.BALLS_POS[x]))
            self.balls[x+1].color = c.COLORS[x]
            self.balls[x+1].number = x+1
        self.stick = Stick(screen)
        self.pockets = []
        self.pockets.append(Pocket(32, 36))
        self.pockets.append(Pocket(398, 24))
        self.pockets.append(Pocket(765, 36))
        self.pockets.append(Pocket(32, 408))
        self.pockets.append(Pocket(398, 420))
        self.pockets.append(Pocket(765, 408))
        self.turn = c.PLAYER1
        self.must_pocket = c.ANY
        self.first_pocket = False
        self.after_hit = False
        self.even_on_pocket = 0
        self.odd_on_pocket = 0
        self.menu = Menu(self.font_medium)
        self.won = False
        self.sound_effect_count = 0
        self.cue_on_pocket = False
        self.sounds_end = False
        self.acknowledge = False
        self.remote_force = 0
        self.remote_angle = 0
        self.stick_movable = True
        
    def draw(self):
        """
        Draw the game elements on the screen.
        """
        for ball in self.balls:
            if not self.menu.is_connected:
                ball.move()
            ball.draw()
        for pocket in self.pockets:
            pocket.draw()
            self.check_pocket(pocket)
        if not self.has_movement(self.balls):
            self.stick.set_angle(self.balls[0], stick_movable=self.stick_movable)  # Update stick position based on stick_movable
            self.stick.draw(self.balls, stick_movable=self.stick_movable)  # Always draw the stick
        self.menu.draw(self.must_pocket, self.won)

    def check_pocket(self, pocket):
        """
        Check if any ball is pocketed in the given pocket.
        
        Args:
            pocket (Pocket): The pocket to check.

        """
        if not self.menu.is_connected:
            for ball in self.balls:
                distance = calc_distance(ball, pocket)
                if distance < pocket.radius:
                    if ball == self.balls[0]:
                        ball.x = -200
                        ball.y = -200
                        ball.velocity = 0
                        self.toggle_turn()
                        self.after_hit = False
                        self.even_on_pocket = len(self.balls_pocket_even)
                        self.odd_on_pocket = len(self.balls_pocket_odd)
                        self.cue_on_pocket = True
                    else:
                        self.balls.remove(ball)
                        if ball.number % 2 == 0:
                            self.balls_pocket_even.append(ball)
                        else:
                            self.balls_pocket_odd.append(ball)
            if self.after_hit and not self.has_movement(self.balls):
                self.after_hit = False
                if (self.even_on_pocket == len(self.balls_pocket_even) and
                    self.odd_on_pocket == len(self.balls_pocket_odd)):
                    self.toggle_turn()
                elif self.must_pocket == c.EVEN and self.odd_on_pocket < len(self.balls_pocket_odd):
                    self.toggle_turn()
                elif self.must_pocket == c.ODD and self.even_on_pocket < len(self.balls_pocket_even):
                    self.toggle_turn()
                self.even_on_pocket = len(self.balls_pocket_even)
                self.odd_on_pocket = len(self.balls_pocket_odd)

    def check_victory(self):
        """
        Check if a player has won the game.
        
        Returns:
            str or False: The winner if there is one, otherwise False.
        
        """
        is_15_ingame = False
        for ball in self.balls:
            if ball.number == 15:
                is_15_ingame = True
        if len(self.balls_pocket_even) == 7 and not is_15_ingame:
            self.won = True
            if self.turn == c.PLAYER1:
                return c.PLAYER1
            else:
                return c.PLAYER2
        elif len(self.balls_pocket_odd) == 8:
            self.won = True
            if self.turn == c.PLAYER1:
                return c.PLAYER1
            else:
                return c.PLAYER2
        elif (not is_15_ingame) and len(self.balls_pocket_even) < 7 and len(self.balls_pocket_odd) < 8:
            self.won = True
            if self.turn == c.PLAYER1:
                return c.PLAYER2
            else:
                return c.PLAYER1
        return False
    
    def click_handle(self, event):
        """
        Handle mouse click events.
        
        Args:
            event (pygame.Event): The event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.menu.click_handle()
            if not self.has_movement(self.balls) and event.button == c.LEFT_CLICK:
                self.stick.is_charging = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if not self.has_movement(self.balls) and event.button == c.LEFT_CLICK:
                self.stick.is_charging = False
                self.stick.hit = True
                self.stick.hit_force = (self.stick.dist_to_ball - 180) * 0.15
            if not self.has_movement(self.balls) and event.button == c.RIGHT_CLICK:
                self.stick.dist_to_ball = 180

        elif event.type == pygame.KEYDOWN:  # Handle key press events
            if event.key == pygame.K_p:
                self.stick_movable = not self.stick_movable
    def toggle_turn(self):
        """
        Toggle the turn between players and set the must_pocket attribute accordingly.
        """
        if self.turn == c.PLAYER1:
            self.turn = c.PLAYER2
        else:
            self.turn = c.PLAYER1
        if self.must_pocket == c.EVEN:
            self.must_pocket = c.ODD
        elif self.must_pocket == c.ODD:
            self.must_pocket = c.EVEN

    def set_player_ball(self):
        """
        After the first pocket, sets if the player is going to pocket EVEN or ODD balls.
        """
        if not self.first_pocket:
            if self.balls_pocket_even:
                self.must_pocket = c.EVEN
                self.first_pocket = True
                
            if self.balls_pocket_odd:
                self.must_pocket = c.ODD
                self.first_pocket = True

    def has_movement(self, objs):
        """
        Check if any of the objects have movement.
        
        Args:
            objs (list): List of objects to check for movement.

        Returns:
            bool: True if any object has movement, False otherwise.
        
        """
        for obj in objs:
            if obj.velocity > 0:
                return True
        if self.balls[0].x < 0:
            self.balls[0].x = 600
            self.balls[0].y = 220
        return False

    def check_collisions(self):
        """
        Check for collisions between balls and handle them.
        """
        for a in self.balls:
            for b in self.balls:
                if a != b and ball_collided(a, b):          
                    p1 = complex(a.x, a.y)
                    v1 = complex(a.velocity*cos(radians(a.angle)), a.velocity*sin(radians(a.angle)))
                    p2 = complex(b.x, b.y)
                    v2 = complex(b.velocity*cos(radians(b.angle)), b.velocity*sin(radians(b.angle)))
                    p12 = p1 - p2
                    d = ((v1 - v2) / p12).real * p12

                    pa = v1 - d
                    polar_a = polar(pa)
                    a.velocity = polar_a[0]
                    a.angle = degrees(polar_a[1])

                    pb = v2 + d
                    polar_b = polar(pb)
                    b.velocity = polar_b[0]
                    b.angle = degrees(polar_b[1])
                    
                    fix_overlap(a, b)       

    def draw_balls_pocket(self):
        """
        Draw balls pocketed after the first pocket.
        """
        x, y, i, j = 420, 455, 0, 0
        for ball in self.balls_pocket_even:
            ball.draw_after_pocket(x+i, y)
            i += 30
        for ball in self.balls_pocket_odd:
            ball.draw_after_pocket(x+j, y+25)
            j += 30

    def sound_effects(self):
        """
        Play sound effects based on game events.
        """
        for a in self.balls:
            for b in self.balls:
                if a != b and ball_collided(a, b):             
                    x = randint(1, 3)
                    if x==1:
                        hit_sound1.play()
                    elif x==2:
                        hit_sound2.play()
                    else:
                        hit_sound3.play()
            ignore = True if (a.x == -200 and a.y == -200) else False           
            if a.x == (c.WIDTH - c.MARGIN_RIGHT) - a.radius:
                hit_wall_sound.play()
            if a.x == a.radius + c.MARGIN_LEFT and not ignore:
                hit_wall_sound.play()
            if a.y == c.HEIGHT - c.MARGIN_BOTTOM - a.radius - c.MENU_HEIGHT:
                hit_wall_sound.play()
            if a.y == a.radius + c.MARGIN_TOP and not ignore:
                hit_wall_sound.play()
        if self.stick.hit and self.stick.dist_to_ball < 200:
            hit_cue_sound.play()
        if len(self.balls) + self.sound_effect_count < 16:
            pocket_sound.play()
            self.sound_effect_count += 1
        if self.cue_on_pocket:
            pocket_sound.play()
            self.cue_on_pocket = False
        if self.menu.winner and not self.sounds_end:
            self.sounds_end = True
            victory_sound.play()
    def event_handle(self, event):
        """
        Handle events for the game.
        
        Args:
            event (pygame.Event): The event to handle.
        
        """
        self.click_handle(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.menu.is_playing = False
                self.menu.is_main_menu = True
            if event.key == pygame.K_p:
                self.stick_follow_mouse = not self.stick_follow_mouse
    def run(self):
        """
        Run the game loop.
        """
        pygame.init()
        screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        pygame.display.set_caption("Billiard Game")
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.event_handle(event)

            screen.fill(c.GREEN)
            self.menu.draw_bg(screen)
            self.check_victory()
            self.set_player_ball()
            self.draw()
            self.draw_balls_pocket()
            self.check_collisions()
            self.sound_effects()

            if not self.has_movement(self.balls):
                if self.stick_follow_mouse:  # Add this condition
                    self.stick.angle = degrees(atan2(pygame.mouse.get_pos()[1] - self.balls[0].y,
                                                     pygame.mouse.get_pos()[0] - self.balls[0].x))
            pygame.display.update()
            clock.tick(c.FPS)  