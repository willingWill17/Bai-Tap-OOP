
def calc_distance(a, b):
    """
    Calculate the distance between two objects.
    
    Args:
        a (object): The first object.
        b (object): The second object.
        
    Returns:
        float: The distance between the two objects.
    """
    return ((a.x - b.x)**2 + (a.y - b.y)**2)**(0.5)


def ball_collided(ball1, ball2):
    """
    Check if two balls have collided.
    
    Args:
        ball1 (Ball): The first ball.
        ball2 (Ball): The second ball.
        
    Returns:
        bool: True if the balls have collided, False otherwise.
    """
    distance = calc_distance(ball1, ball2)
    if distance <= (ball1.radius + ball2.radius):
        return True
    else:
        return False


def fix_overlap(ball1, ball2):
    """
    Adjust the positions of two balls to fix overlap.
    
    Args:
        ball1 (Ball): The first ball.
        ball2 (Ball): The second ball.
    """
    distance = calc_distance(ball1, ball2)
    while distance <= (ball1.radius + ball2.radius + 1):
        if ball1.x > ball2.x:
            ball1.x += 0.1
        else:
            ball1.x -= 0.1
        if ball1.y > ball2.y:
            ball1.y += 0.1
        else:
            ball1.y -= 0.1
        distance = calc_distance(ball1, ball2)
import pygame
import billiards.constants as c
import sys
from billiards.game import Game
from billiards.menu import Menu
from billiards.stick import Stick
import pickle
pygame.init()
background_img = pygame.image.load('assets/table.png')
stick_img = pygame.image.load('assets/stick.png')
icon_img = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon_img)

conn = None
client_socket = None

font = pygame.font.Font('freesansbold.ttf', 10)
font_medium = pygame.font.Font('freesansbold.ttf', 16)
screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
pygame.display.set_caption("Pool Billiards")
hit_sound1 = pygame.mixer.Sound(r"assets/hit1.wav")
hit_sound2 = pygame.mixer.Sound(r"assets/hit2.wav")
hit_sound3 = pygame.mixer.Sound(r"assets/hit3.wav")
pocket_sound = pygame.mixer.Sound(r"assets/pocket.wav")
hit_cue_sound = pygame.mixer.Sound(r"assets/hit_cue.wav")
hit_wall_sound = pygame.mixer.Sound(r"assets/wall_hit.wav")
victory_sound = pygame.mixer.Sound(r"assets/victory.wav")

game = Game(screen,font_medium)
Stick(screen,game)
Menu(game,font_medium)
clock = pygame.time.Clock()
old_time = 0

while True:
    screen.fill(c.WHITE)
    screen.blit(background_img, (0, 0))
    for event in pygame.event.get():
        if not game.won:
            game.click_handle(event)
        if event.type == pygame.QUIT:  
            pygame.quit()
            if game.menu.is_hosting:
                conn.close()
            elif game.menu.is_connected:
                client_socket.disconnect()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                tmp_connected = game.menu.is_connected
                tmp_hosting = game.menu.is_hosting
                game = Game(screen,font_medium)
                game.menu.is_connected = tmp_connected
                game.menu.is_hosting = tmp_hosting
    game.set_player_ball()
    if not game.menu.is_connected:
        game.check_collisions()
    game.draw_balls_pocket()
    if (not game.menu.is_connected and not game.menu.is_hosting) or (game.menu.is_hosting and game.turn == c.PLAYER1) or (game.menu.is_connected and game.turn == c.PLAYER2):
        game.stick.set_angle(game.balls[0])
    time_now = pygame.time.get_ticks()
    if  time_now > old_time + 8:
        game.draw()
        game.sound_effects()
    
    if game.menu.is_connected:
        try:
            data = client_socket.recv(4096)
            if data:
                balls_host, balls_host_even, balls_host_odd, mouse_pos, turn, pocket_type, ack = pickle.loads(data)
                game.balls = balls_host.copy()
                game.balls_pocket_even = balls_host_even.copy()
                game.balls_pocket_odd = balls_host_odd.copy()
                if game.turn == c.PLAYER1:
                    game.stick.set_angle(game.balls[0], mouse_pos)
                game.turn = turn
                game.must_pocket = pocket_type
                if ack:
                    game.remote_force = 0
                    game.remote_angle = 0
                if game.stick.remote_hit:
                    game.stick.remote_hit = False
                    game.remote_force = game.stick.hit_force
                    game.remote_angle = game.stick.angle
                    print("Remote hit sent with force {} and angle {}".format(game.remote_force, game.remote_angle))
                mouse_pos = pygame.mouse.get_pos()
                data = pickle.dumps((game.remote_force, game.remote_angle, mouse_pos))
                client_socket.send(data)
        except Exception as e:
            pass

    if game.menu.is_hosting:
        mouse_pos = pygame.mouse.get_pos()
        data = pickle.dumps((game.balls, game.balls_pocket_even, game.balls_pocket_odd, mouse_pos, game.turn, game.must_pocket, game.acknowledge))
        try:
            conn.send(data)
            data = conn.recv(4096)
            if data:
                force, angle, mouse_pos = pickle.loads(data)
                if force and game.turn == c.PLAYER2 and not game.has_movement(game.balls):
                    game.balls[0].set_force_angle(force, angle)
                    game.stick.hit = False
                    game.after_hit = True
                    game.acknowledge = True
                else:
                    game.acknowledge = False
                if game.turn == c.PLAYER2:
                    game.stick.set_angle(game.balls[0], mouse_pos)
        except Exception as e:
            pass
    clock.tick()
    if  time_now > old_time + 8:
        old_time = time_now
        pygame.display.flip()
        
        
