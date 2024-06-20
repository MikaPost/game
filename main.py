import pygame
import random


def lylchudem():
    icon = pygame.image.load("images/icon.png").convert_alpha()
    bg = pygame.image.load("images\\bg.png").convert()
    ghost = pygame.image.load("images/ghost.png").convert_alpha()
    walk_right = [pygame.image.load("images\\player_right\\player_right1.png").convert_alpha(),
                  pygame.image.load("images\\player_right\\player_right2.png").convert_alpha(),
                  pygame.image.load("images\\player_right\\player_right3.png").convert_alpha(),
                  pygame.image.load("images\\player_right\\player_right4.png").convert_alpha()
                  ]
    walk_left = [pygame.image.load("images/player_left/player_left1.png").convert_alpha(),
                 pygame.image.load("images/player_left/player_left2.png").convert_alpha(),
                 pygame.image.load("images/player_left/player_left4.png").convert_alpha(),
                 pygame.image.load("images/player_left/player_left3.png").convert_alpha()
                 ]
    game_over_font = pygame.font.Font("game-stage-game-stage-regular-400.ttf", 100)
    font = pygame.font.Font("game-stage-game-stage-regular-400.ttf", 60)
    bullet = pygame.image.load("images/kunay.png").convert_alpha()
    return icon, bg, ghost, walk_right, walk_left, game_over_font, font, bullet


def player_movement(keys, player_x, player_y, is_jump, jump_count, player_speed, screen, walk_left, walk_right,
                    player_anim_count):
    # Handle left/right movement
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and player_x < 775:
        player_x += player_speed

    # Draw player
    if keys[pygame.K_LEFT]:
        screen.blit(walk_left[player_anim_count], (player_x, player_y))
    else:
        screen.blit(walk_right[player_anim_count], (player_x, player_y))

    # Handle jumping
    if not is_jump:
        if keys[pygame.K_UP]:
            is_jump = True
    else:
        if jump_count >= -8:
            neg = 1 if jump_count > 0 else -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 8

    return player_x, player_y, is_jump, jump_count


def handle_bullets(bullets, ghost_list_in_game, bullet_image, screen, bullets_left, point):
    for i, el in enumerate(bullets):
        screen.blit(bullet_image, (el.x, el.y))
        el.x += 7

        if el.x > 800:
            bullets.pop(i)
            bullets_left += 1
            break

        if ghost_list_in_game:
            for (index, ghost_el) in enumerate(ghost_list_in_game):
                if el.colliderect(ghost_el):
                    point += 1
                    ghost_list_in_game.pop(index)
                    bullets.pop(i)
                    bullets_left += 1
                    break  # Break to avoid modifying the list during iteration

    return bullets_left, point


def handle_ghosts(ghost_list_in_game, ghost_image, screen, player_rect):
    for i, el in enumerate(ghost_list_in_game):
        screen.blit(ghost_image, el)
        el.x -= 10

        if el.x < -10:
            ghost_list_in_game.pop(i)

        if player_rect.colliderect(el):
            return False

    return True


def main():
    pygame.init()

    clock = pygame.time.Clock()

    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Game")

    icon, bg, ghost, walk_right, walk_left, game_over_font, font, bullet = lylchudem()

    pygame.display.set_icon(icon)

    ghost_list_in_game = []

    player_anim_count = 0
    bg_x = 0

    player_speed = 7
    player_x = 150
    player_y = 434

    is_jump = False
    jump_count = 8

    point = 0

    ghost_timer = pygame.USEREVENT + 2
    # Set initial ghost spawn time to a random value
    pygame.time.set_timer(ghost_timer, random.randint(1000, 3000))


    bullets_left = 3  # Use a list to pass by reference
    bullets = []

    gameplay = False
    running = True
    while running:
        # Draw background
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + 800, 0))

        point_label = font.render(("Point: " + str(point)), False, (148, 87, 235))
        screen.blit(point_label, (20, 20))

        # If the player has not lost yet
        if gameplay:
            player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

            # Handle ghosts
            if ghost_list_in_game:
                gameplay = handle_ghosts(ghost_list_in_game, ghost, screen, player_rect)

            # Handle player movement
            keys = pygame.key.get_pressed()
            player_x, player_y, is_jump, jump_count = player_movement(keys, player_x, player_y, is_jump, jump_count,
                                                                      player_speed, screen, walk_left, walk_right,
                                                                      player_anim_count)

            # Handle bullets
            bullets_left, point = handle_bullets(bullets, ghost_list_in_game, bullet, screen, bullets_left, point)

            # Update player animation count
            if player_anim_count >= 3:
                player_anim_count = 0
            else:
                player_anim_count += 1

            # Scroll background
            bg_x -= 5
            if bg_x <= -800:
                bg_x = 0
        else:
            lose_label = game_over_font.render("GAME OVER", False, (235, 76, 66))
            restart_label = font.render("Play again", False, (139, 235, 154))
            restart_label_rect = restart_label.get_rect(topleft=(240, 270))

            screen.fill((67, 89, 112))
            screen.blit(lose_label, (100, 150))
            screen.blit(point_label, (20, 20))
            screen.blit(restart_label, restart_label_rect)

            # Handle mouse click on restart button
            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                gameplay = True
                player_x = 150
                bg_x = 0
                point = 0
                ghost_list_in_game.clear()
                bullets.clear()
                bullets_left = 3

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == ghost_timer:
                random_y = random.randint(300, 500)
                ghost_list_in_game.append(ghost.get_rect(topleft=(800, random_y)))
                pygame.time.set_timer(ghost_timer, random.randint(500, 3000))

            if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and bullets_left > 0:
                bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 15)))
                bullets_left -= 1

        clock.tick(15)


if __name__ == "__main__":
    main()
