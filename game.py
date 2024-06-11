import pygame
from constants import *

class Game:
    
    def all_balls_stationary(self,balls, threshold=0.1):
        """
        Checks if all balls are stationary within a given threshold.

        Args:
            balls (list): List of ball objects.
            threshold (float, optional): Threshold for velocity magnitude. Defaults to 0.1.

        Returns:
            bool: True if all balls are stationary, False otherwise.
        """
        for ball in balls:
            if ball.body.velocity.length > threshold:
                return False
        return True
    def redraw_window(self,screen,balls,ball_images):
        """
        Redraws the game window.

        Parameters
        ----------
        screen : pygame.Surface
            The screen to redraw.
        balls : list
            The list of balls to draw on the screen.
        """

        screen.blit(pygame.image.load("Assets/images/table_image.png").convert_alpha(), (0, 0))
        for i, ball in enumerate(balls):
            screen.blit(ball_images[i], (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))
        pygame.draw.rect(screen, (50, 50, 50), (0, SCREEN_HEIGHT, SCREEN_WIDTH, BOTTOM_PANEL))
        pygame.display.update()
    def display_game_over(self,screen,turn,player1,player2):
        """
        Displays the game over screen.

        Parameters
        ----------
        screen : pygame.Surface
            The screen to display the game over screen on.
        turn : int
            The current turn number.
        player1 : list
            The list of balls for player 1.
        player2 : list
            The list of balls for player 2.
        play_func : function
            The function to call to play the game.
        """
        
        if turn == 1 and len(player1) == 7:
            game_over_text = "Player 1 Wins!"
        elif turn == 2 and len(player2) == 7:
            game_over_text = "Player 2 Wins!"
        else:
            if turn == 1:
                game_over_text = "Player 2 Wins!"
            else:
                game_over_text = "Player 1 Wins!"
        victory_sound = pygame.mixer.Sound(r"Assets/victory.wav")
        pygame.mixer.Sound.play(victory_sound)
        game_over_surface = pygame.font.SysFont('tempussansitc',100).render(game_over_text, True, "#b68f40")
        game_over_rect = game_over_surface.get_rect(center=(640, 300))
        screen.blit(game_over_surface, game_over_rect)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    pygame.quit()
