import pymunk
from constants import *
class Create:
    def create_cushion(self,poly_dims,space):
        """
        Creates a cushion with given dimensions.

        Parameters:
            poly_dims (list): List of points defining the polygon shape of the cushion.
        """
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (0, 0)
        shape = pymunk.Poly(body, poly_dims)
        shape.elasticity = 0.8
        space.add(body, shape) 
    def draw_text(self,text, font, text_col, x, y,screen):
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
    def create_ball(self,radius, pos,static_body,space):
        """
        Creates a ball with a given radius and position.

        Parameters:
            radius (int): The radius of the ball.
            pos (tuple): The position of the ball.

        Returns:
            pymunk.Circle: The created ball shape.
        """
        body = pymunk.Body()    
        body.position = pos
        shape = pymunk.Circle(body, radius)
        shape.mass = 3
        shape.elasticity = 0.8
        # Use Pivot Joint to add Friction
        pivot = pymunk.PivotJoint(static_body, body, (0, 0), (0, 0))
        pivot.max_bias = 0  # Disable Joint correction
        pivot.max_force = 1000  # Emulate Linear Friction
        space.add(body, shape, pivot)
        return shape
