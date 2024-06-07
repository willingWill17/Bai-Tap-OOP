SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 680
BOTTOM_PANEL = 50
FPS = 120
dia = 36
force = 0
pocket_dia = 66
max_force = 10000
current_player = 1
force_direction = 1
game_running = True
cue_ball_potted = False
taking_shot = True
powering_up = False
potted_balls = []
player1_balls = []
player2_balls = []

BG = (50, 50, 50)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

smooth=[1,2,3,4,5,6,7]
non_smooth=[9,10,11,12,13,14,15]
balls = []
rows = 5
pos = (888, SCREEN_HEIGHT / 2)

pockets = [
    (55, 63),
    (592, 48),
    (1134, 64),
    (55, 616),
    (592, 629),
    (1134, 616)
]

cushions = [
    [(88, 56), (109, 77), (555, 77), (564, 56)],
    [(621, 56), (630, 77), (1081, 77), (1102, 56)],
    [(89, 621), (110, 600), (556, 600), (564, 621)],
    [(622, 621), (630, 600), (1081, 600), (1102, 621)],
    [(56, 96), (77, 117), (77, 560), (56, 581)],
    [(1143, 96), (1122, 117), (1122, 560), (1143, 581)],
]
