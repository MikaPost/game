"""
This file is for our new theme: game
Created by: Miqayel Postoyan
Date: 28 June
"""
import pygame
import random


def get_image():
    """
    Function: get_image
    Brief: Loads and returns various game images and fonts.
    Params: None
    Return: Tuple containing game images and fonts
    """
    # Loading images and fonts
    icon = pygame.image.load("images/icon.png").convert_alpha()
    bg = pygame.image.load("images/bg.png").convert()
    ghost = pygame.image.load("images/ghost.png").convert_alpha()
    # Loading player images for walking animations
    walk_right = [pygame.image.load("images/player_right/player_right1.png").convert_alpha(),
                  pygame.image.load("images/player_right/player_right2.png").convert_alpha(),
                  pygame.image.load("images/player_right/player_right3.png").convert_alpha(),
                  pygame.image.load("images/player_right/player_right4.png").convert_alpha()
                  ]
    walk_left = [pygame.image.load("images/player_left/player_left1.png").convert_alpha(),
                 pygame.image.load("images/player_left/player_left2.png").convert_alpha(),
                 pygame.image.load("images/player_left/player_left4.png").convert_alpha(),
                 pygame.image.load("images/player_left/player_left3.png").convert_alpha()
                 ]
    # Loading fonts
    game_over_font = pygame.font.Font("game-stage-game-stage-regular-400.ttf", 100)
    font = pygame.font.Font("game-stage-game-stage-regular-400.ttf", 60)
    # Loading bullet image
    bullet = pygame.image.load("images/kunay.png").convert_alpha()
    return icon, bg, ghost, walk_right, walk_left, game_over_font, font, bullet


def player_movement(keys, player_x, player_y, is_jump, jump_count, player_speed, screen, walk_left, walk_right,
                    player_anim_count):
    """
    Function: player_movement
    Brief: Handles player movement and jumping.
    Params:
        keys (pygame.key.get_pressed()): Dictionary of currently pressed keys
        player_x (int): X-coordinate of the player
        player_y (int): Y-coordinate of the player
        is_jump (bool): Flag indicating if the player is jumping
        jump_count (int): Counter for the jump animation
        player_speed (int): Speed of the player's horizontal movement
        screen (pygame.Surface): Surface to draw on
        walk_left (list): List of left-facing player images
        walk_right (list): List of right-facing player images
        player_anim_count (int): Index of the current player animation frame
    Return:
        Updated player coordinates and jump state
    """
    # Handling horizontal movement
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and player_x < 775:
        player_x += player_speed

    # Displaying player images based on movement direction
    if keys[pygame.K_LEFT]:
        screen.blit(walk_left[player_anim_count], (player_x, player_y))
    else:
        screen.blit(walk_right[player_anim_count], (player_x, player_y))

    # Handling jumping mechanics
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
    """
    Function: handle_bullets
    Brief: Handles bullet movement, collision detection, and scoring.
    Params:
        bullets (list): List of active bullet rectangles
        ghost_list_in_game (list): List of active ghost rectangles
        bullet_image (pygame.Surface): Image of the bullet
        screen (pygame.Surface): Surface to draw on
        bullets_left (int): Number of bullets left
        point (int): Current score
    Return:
        Updated bullet count and score
    """
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
                    break

    return bullets_left, point


def handle_ghosts(ghost_list_in_game, ghost_image, screen, player_rect):
    """
    Function: handle_ghosts
    Brief: Handles ghost movement and collision with the player.
    Params:
        ghost_list_in_game (list): List of active ghost rectangles
        ghost_image (pygame.Surface): Image of the ghost
        screen (pygame.Surface): Surface to draw on
        player_rect (pygame.Rect): Rectangle representing the player
    Return:
        Boolean indicating if the game should continue (True) or end (False)
    """
    for i, el in enumerate(ghost_list_in_game):
        screen.blit(ghost_image, el)
        el.x -= 10

        if el.x < -10:
            ghost_list_in_game.pop(i)

        if player_rect.colliderect(el):
            return False

    return True


def main():
    """
    Function: main
    Brief: Entry point of the program.
    """
    pygame.init()  # Initialize pygame modules

    clock = pygame.time.Clock()  # Create a clock object to control the frame rate

    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))  # Create the game window
    pygame.display.set_caption("Game")  # Set the window title

    # Load game assets (images, fonts)
    icon, bg, ghost, walk_right, walk_left, game_over_font, font, bullet = get_image()
    pygame.display.set_icon(icon)  # Set the window icon

    ghost_list_in_game = []  # List to store active ghosts

    player_anim_count = 0  # Counter for player animation frames
    bg_x = 0  # Initial position of the background

    player_speed = 7  # Horizontal movement speed of the player
    player_x = 150  # Initial X position of the player
    player_y = 434  # Initial Y position of the player

    is_jump = False  # Flag indicating if the player is jumping
    jump_count = 8  # Counter for jump animation

    point = 0  # Player's score

    ghost_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(ghost_timer, random.randint(1000, 3000))  # Timer for spawning ghosts

    bullets_left = 3  # Number of bullets the player has
    bullets = []  # List to store active bullets

    gameplay = True  # Flag to control the game loop
    running = True  # Flag to control the main program loop
    while running:
        # Game loop

        # Draw background
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + 800, 0))

        # Display player's score
        point_label = font.render(("Point: " + str(point)), False, (148, 87, 235))
        screen.blit(point_label, (20, 20))

        if gameplay:
            # Game in progress

            # Get player's rectangle for collision detection
            player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

            # Handle active ghosts
            if ghost_list_in_game:
                gameplay = handle_ghosts(ghost_list_in_game, ghost, screen, player_rect)

            # Handle player movement and jumping
            keys = pygame.key.get_pressed()
            player_x, player_y, is_jump, jump_count = player_movement(keys, player_x, player_y, is_jump, jump_count,
                                                                      player_speed, screen, walk_left, walk_right,
                                                                      player_anim_count)

            # Handle bullets
            bullets_left, point = handle_bullets(bullets, ghost_list_in_game, bullet, screen, bullets_left, point)

            # Animate player
            if player_anim_count >= 3:
                player_anim_count = 0
            else:
                player_anim_count += 1

            # Scroll the background
            bg_x -= 5
            if bg_x <= -800:
                bg_x = 0

        else:
            # Game over screen

            # Display "Game Over" label and "Play again" option
            lose_label = game_over_font.render("GAME OVER", False, (235, 76, 66))
            restart_label = font.render("Play again", False, (139, 235, 154))
            restart_label_rect = restart_label.get_rect(topleft=(240, 270))

            screen.fill((67, 89, 112))
            screen.blit(lose_label, (100, 150))
            screen.blit(point_label, (20, 20))
            screen.blit(restart_label, restart_label_rect)

            # Check if "Play again" is clicked
            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                # Reset game state on restart
                gameplay = True
                player_x = 150
                bg_x = 0
                point = 0
                ghost_list_in_game.clear()
                bullets.clear()
                bullets_left = 3

        pygame.display.update()  # Update the display

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Quit the main loop on window close
                pygame.quit()  # Clean up pygame resources

            # Timer event for spawning ghosts
            if event.type == ghost_timer:
                random_y = random.randint(300, 500)
                ghost_list_in_game.append(ghost.get_rect(topleft=(800, random_y)))
                pygame.time.set_timer(ghost_timer, random.randint(500, 3000))

            # Handle shooting bullets
            if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and bullets_left > 0:
                bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 15)))
                bullets_left -= 1

        clock.tick(15)  # Cap the frame rate to 15 frames per second


if __name__ == "__main__":
    main()
