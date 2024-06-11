class Button():
    """
    A class to represent a button in a pygame application.

    Attributes
    ----------
    image : pygame.Surface
        The image of the button.
    x_pos : int
        The x-coordinate of the button's center.
    y_pos : int
        The y-coordinate of the button's center.
    font : pygame.font.Font
        The font of the button's text.
    base_color : tuple
        The RGB color of the button's text when not hovering.
    hovering_color : tuple
        The RGB color of the button's text when hovering.
    """

    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input

        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
    def update(self, screen):    
        """
        Blits the button's image and text onto the given screen.

        Parameters
        ----------
        screen : pygame.Surface
            The screen to blit the button's image and text onto.
        """
        
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        """
        Checks if the given position is within the button's area.

        Parameters
        ----------
        position : tuple
            The position to check.

        Returns
        -------
        bool
            True if the position is within the button's area, False otherwise.
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        """
        Changes the color of the button's text based on the given position.

        Parameters
        ----------
        position : tuple
            The position to base the color change on.
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)