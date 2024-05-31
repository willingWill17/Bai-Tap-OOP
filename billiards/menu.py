import pygame
from label import Label
import constants as c

class Menu:
    def __init__(self,game,font_medium):
        """
        Initialize a Menu object.
        """
        self.font_medium= font_medium
        self.game=game
        self.is_hosting = False
        self.is_connected = False
        self.lbl_player = Label(200, 460, font_medium,"")
        self.winner = 0

    def draw(self, must_pocket, won):
        """
        Draw the menu on the screen.
        
        Args:
            must_pocket: Indicates the type of balls that must be pocketed (EVEN, ODD, or ANY).
            won (bool): Indicates if the game has been won.
        """
        winner = False
        text = ""
        if must_pocket == c.EVEN:
            ball_type = "EVEN"
        elif must_pocket == c.ODD:
            ball_type = "ODD"
        else:
            ball_type = "ANY"
        if not self.winner:
            text = "Player {} Turn ({})".format(self.game.turn, ball_type)
            self.winner = self.game.check_victory()
        if self.winner:
            text = "Player {} won the game!".format(self.winner)
        self.lbl_player.draw(self.screen, text)

    def click_handle(self):
        pass
