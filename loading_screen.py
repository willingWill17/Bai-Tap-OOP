import pygame, sys
from button import Button
from play import Play
class Screen:

    def main_menu(self):
        """
        Displays the main menu of the game. This function initializes the main menu screen with buttons for playing the game and quitting the application.
        
        The main menu includes:
        - A background image.
        - A title text "MAIN MENU".
        - Two buttons: "PLAY" to start the game and "QUIT" to exit the application.

        The function continuously runs to check for user interactions with the buttons and updates the screen accordingly.
        """
        pygame.init()
        SCREEN = pygame.display.set_mode((1280, 720))
        BG = pygame.image.load("Assets/images/Post.png")  
        pygame.display.set_caption("PoolGame")
        while True:
            SCREEN.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            PLAY_BUTTON = Button(image=pygame.image.load("Assets/images/Play Rect.png"), pos=(640, 350), 
                                text_input="PLAY", font=pygame.font.SysFont('freestylescript',75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("Assets/images/Quit Rect.png"), pos=(640, 550), 
                                text_input="QUIT", font=pygame.font.SysFont('freestylescript',75), base_color="#d7fcd4", hovering_color="White")

            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        Play().play()

                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
# Screen().main_menu()