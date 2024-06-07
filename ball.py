import pymunk
from constants import SCREEN_HEIGHT
def create_ball(radius, pos,static_body,space):
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
