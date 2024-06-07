
def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + BOTTOM_PANEL))
    pygame.display.set_caption("PoolGame")

    space = pymunk.Space()
    static_body = space.static_body
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    clock = pygame.time.Clock()

    font = pygame.font.SysFont("script", 30)
    large_font = pygame.font.SysFont("Lato", 60)

    table_image = pygame.image.load("Assets/images/table.png").convert_alpha()
    ball_images = []
    for i in range(1, 17):
        ball_image = pygame.image.load(f"Assets/images/ball_{i}.png").convert_alpha()
        ball_images.append(ball_image)

    pray = {}
    # Potting Balls
    j = 0
    for col in range(5):
        for row in range(rows):
            pos = (250 + (col * (dia + 1)), 267 + (row * (dia + 1)) + (col * dia / 2))
            new_ball = create_ball(dia / 2, pos, static_body, space)
            j += 1
            pray[new_ball] = j
            balls.append(new_ball)
        rows -= 1

    cue_ball = create_ball(dia / 2, (888, SCREEN_HEIGHT / 2), static_body, space)
    balls.append(cue_ball)

    for c in cushions:
        create_cushion(c, space)

    cue = Cue(balls[-1].body.position)

    # Create Power Bars
    power_bar = pygame.Surface((10, 20))
    power_bar.fill(RED)
    first = None

    # Game Loop
    run = True
    while run:
        clock.tick(FPS)
        space.step(1 / FPS)

        # Fill Background
        screen.fill(BG)

        # Draw Pool Table
        screen.blit(table_image, (0, 0))

        for i, ball in enumerate(balls):
            for pocket in pockets:
                ball_x_dist = abs(ball.body.position[0] - pocket[0])
                ball_y_dist = abs(ball.body.position[1] - pocket[1])
                ball_dist = math.sqrt((ball_x_dist ** 2) + (ball_y_dist ** 2))
                if ball_dist <= pocket_dia / 2:
                    if i == len(balls) - 1:
                        cue_ball_potted = True
                        ball.body.position = (-100, -100)
                        ball.body.velocity = (0.0, 0.0)
                    else:
                        if first is None:
                            first = current_player
                            if first == 1:
                                if i + 1 in smooth:
                                    player1_type = 'smooth'
                                    player2_type = 'non_smooth'
                                else:
                                    player1_type = 'non_smooth'
                                    player2_type = 'smooth'
                            if first == 2:
                                if i + 1 in smooth:
                                    player2_type = 'smooth'
                                    player1_type = 'non_smooth'
                                else:
                                    player2_type = 'non_smooth'
                                    player1_type = 'smooth'
                        space.remove(ball.body)
                        balls.remove(ball)
                        if pray[ball] in smooth:
                            if player1_type == 'smooth':
                                player1_balls.append(ball_images[i])
                            else:
                                player2_balls.append(ball_images[i])
                        else:
                            if player1_type == 'non_smooth':
                                player1_balls.append(ball_images[i])
                            else:
                                player2_balls.append(ball_images[i])
                        print('-------------------------------------------')
                        print(player1_balls)
                        print(player2_balls)
                        ball_images.pop(i)

        for i, ball in enumerate(balls):
            screen.blit(ball_images[i], (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))

        taking_shot = True
        for ball in balls:
            if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0:
                taking_shot = False

        if taking_shot and game_running:
            if cue_ball_potted:
                balls[-1].body.position = (888, SCREEN_HEIGHT / 2)
                cue_ball_potted = False

            mouse_pos = pygame.mouse.get_pos()
            cue.rect.center = balls[-1].body.position
            x_dist = balls[-1].body.position[0] - mouse_pos[0]
            y_dist = -(balls[-1].body.position[1] - mouse_pos[1])
            cue_angle = math.degrees(math.atan2(y_dist, x_dist))
            cue.update(cue_angle)
            cue.draw(screen)

        if powering_up and game_running:
            force += 100 * force_direction
            if force >= max_force or force <= 0:
                force_direction *= -1

            for b in range(math.ceil(force / 2000)):
                screen.blit(power_bar,
                            (balls[-1].body.position[0] - 30 + (b * 15),
                             balls[-1].body.position[1] + 30))

        elif not powering_up and taking_shot:
            x_impulse = math.cos(math.radians(cue_angle))
            y_impulse = math.sin(math.radians(cue_angle))
            balls[-1].body.apply_impulse_at_local_point((force * -x_impulse, force * y_impulse), (0, 0))
            force = 0
            force_direction = 1

        pygame.draw.rect(screen, BG, (0, SCREEN_HEIGHT, SCREEN_WIDTH, BOTTOM_PANEL))

        for i, ball in enumerate(player1_balls):
            screen.blit(ball, (10 + (i * 50), SCREEN_HEIGHT + 10))
        for j, llab in enumerate(player2_balls):
            screen.blit(llab, ((SCREEN_WIDTH) / 2 + j * 50 + 150, SCREEN_HEIGHT + 10))

        if len(balls) == 1:
            draw_text("YOU WIN!", large_font, WHITE, SCREEN_WIDTH / 2 - 160, SCREEN_HEIGHT / 2 - 100, screen)
            game_running = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and taking_shot:
                powering_up = True

            if event.type == pygame.MOUSEBUTTONUP and taking_shot:
                powering_up = False
                current_player = 1 if current_player == 2 else 2

            if event.type == pygame.QUIT:
                run = False

        text_surface = font.render("Player " + str(current_player) + "'s turn", True, (255, 255, 255))
        screen.blit(text_surface, ((SCREEN_WIDTH - text_surface.get_width() - 10) // 2, SCREEN_HEIGHT))
        pygame.display.update()

    pygame.quit()
if __name__ == "__main__":
    import math
    import pygame
    import pymunk
    import pymunk.pygame_util
    from constants import *
    from cushion import create_cushion
    from cue import Cue
    from ball import create_ball
    from text import draw_text
    main()