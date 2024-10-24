# ************************************
# Python Snake
# ************************************
import pygame
import random
import os  # For file operations

# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Snake block size
SNAKE_BLOCK = 10

# Snake speed
SNAKE_SPEED = 15

# Highscore file path
HIGHSCORE_FILE = "highscore.txt"

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Define the clock
clock = pygame.time.Clock()

# Set the font for text display
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Function to display score
def display_score(score, highscore):
    value = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(value, [0, 0])
    highscore_value = score_font.render(f"Highscore: {highscore}", True, WHITE)
    screen.blit(highscore_value, [0, 40])

# Function to draw the snake
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])

# Message function for game over screen
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3])

# Function to get the highscore from file
def get_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0  # If the file is empty or contains invalid data, return 0
    else:
        return 0

# Function to save the highscore to file
def save_highscore(highscore):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(highscore))

# Main game loop
def game_loop():
    game_over = False
    game_close = False

    # Starting position of the snake
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    # Starting movement direction
    x_change = 0
    y_change = 0

    # Snake body
    snake_list = []
    length_of_snake = 1

    # Randomize food position
    food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    # Get the current highscore
    highscore = get_highscore()

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            message("You Died! Press Q to Quit or R to Restart", RED)
            display_score(length_of_snake - 1, highscore)
            pygame.display.update()

            # Save the highscore if the current score is greater
            if length_of_snake - 1 > highscore:
                highscore = length_of_snake - 1
                save_highscore(highscore)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        game_loop()  # Restart the game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x_change = -SNAKE_BLOCK
                    y_change = 0
                elif event.key == pygame.K_d:
                    x_change = SNAKE_BLOCK
                    y_change = 0
                elif event.key == pygame.K_w:
                    y_change = -SNAKE_BLOCK
                    x_change = 0
                elif event.key == pygame.K_s:
                    y_change = SNAKE_BLOCK
                    x_change = 0

        if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
            game_close = True
        x += x_change
        y += y_change
        screen.fill(BLACK)

        pygame.draw.rect(screen, WHITE, [food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK])
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Removed game over condition for snake colliding with itself

        draw_snake(SNAKE_BLOCK, snake_list)
        display_score(length_of_snake - 1, highscore)

        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

# Start the game
game_loop()
