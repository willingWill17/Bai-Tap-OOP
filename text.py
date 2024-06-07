def draw_text(text, font, text_col, x, y,screen):
    """
    Renders text on the screen at the specified coordinates.

    Parameters:
        text (str): The text to render.
        font (pygame.font.Font): The font to use for rendering.
        text_col (tuple): The color of the text.
        x (int): The x-coordinate of the text position.
        y (int): The y-coordinate of the text position.
    """
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))