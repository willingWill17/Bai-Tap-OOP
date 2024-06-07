import pymunk  

def create_cushion(poly_dims,space):
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
