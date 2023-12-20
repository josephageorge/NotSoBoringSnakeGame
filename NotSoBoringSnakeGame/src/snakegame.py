import pygame
import time
import random

pygame.init()

# Set up the game window
width, height = 600, 400
game_window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Define colors
background_color = (44, 62, 80)  # Dark blue-gray
border_color = (52, 73, 94)  # Lighter blue-gray
snake_head_color = (231, 76, 60)  # Red
snake_body_color = (255, 165, 0)  # Orange
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (0, 0, 0)
rock_color = (0, 0, 0)

# Snake properties
snake_block = 10
snake_speed = 15

# Initialize the clock
clock = pygame.time.Clock()

# Function to draw the snake with different head and body colors
def draw_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        color = snake_head_color if i == len(snake_list) - 1 else snake_body_color
        pygame.draw.rect(game_window, color, [x[0], x[1], snake_block, snake_block])


def display_score(score):
    font = pygame.font.SysFont(None, 30)
    value = font.render("Your Score: " + str(score), True, white)
    shadow = font.render("Your Score: " + str(score), True, black)
    game_window.blit(shadow, [5, 5])  
    game_window.blit(value, [0, 0])


def display_message(message):
    font = pygame.font.SysFont(None, 30)
    value = font.render(message, True, white)
    shadow = font.render(message, True, black)
    game_window.blit(shadow, [width / 2 - 150 + 2, height / 2 + 2])  
    game_window.blit(value, [width / 2 - 150, height / 2])

# Motion to run the game :D
def game_loop():
    global snake_speed

    game_over = False
    game_close = False

    # Snake lol
    x1, y1 = width / 2, height / 2
    x1_change, y1_change = 0, 0

    # Length, change later for "power-up/rock"
    snake_list = []
    length_of_snake = 1

    # Initialize the position of the moving apple
    apple_x, apple_y = round(random.randrange(0, width - snake_block) / 10.0) * 10.0, round(random.randrange(0, height - snake_block) / 10.0) * 10.0
    apple_speed = 3  # Speed of the moving apple

    # position of power-up
    rock_x, rock_y = 0, 0
    rock_active = False

    display_message_flag = False

    while not game_over:

        while game_close:
            game_window.fill(background_color)
            display_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_s:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Update the position of the snake
        x1 += x1_change
        y1 += y1_change

        # Check for collisions with the window boundaries
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        # Update the game window
        game_window.fill(background_color)
        pygame.draw.rect(game_window, border_color, (0, 0, width, height), 5)

        # Move the apple towards a random direction
        if random.choice([True, False]):
            if x1 < apple_x:
                apple_x -= apple_speed
            elif x1 > apple_x:
                apple_x += apple_speed
        else:
            if y1 < apple_y:
                apple_y -= apple_speed
            elif y1 > apple_y:
                apple_y += apple_speed

        # Check if the snake catches the moving apple
        if x1 == apple_x and y1 == apple_y:
            length_of_snake += 1
            apple_x, apple_y = round(random.randrange(0, width - snake_block) / 10.0) * 10.0, round(random.randrange(0, height - snake_block) / 10.0) * 10.0

            # Randomly spawn a power-up
            if random.choice([True, False]) and not rock_active:
                rock_x, rock_y = round(random.randrange(0, width - snake_block) / 10.0) * 10.0, round(random.randrange(0, height - snake_block) / 10.0) * 10.0
                rock_active = True

            # Randomly set the display_message_flag to True
            display_message_flag = random.choice([True, False])

        # Draw the power-up
        if rock_active:
            pygame.draw.rect(game_window, yellow, [rock_x, rock_y, snake_block + 10, snake_block + 10])

            # Check if the snake catches the block
            if x1 == rock_x and y1 == rock_y:
                rock_active = False
                display_message("Uh oh...I think you lost your tail")
                length_of_snake -= 1
                snake_list.pop()
                pygame.display.update()
                time.sleep(2)

        pygame.draw.rect(game_window, red, [apple_x, apple_y, snake_block, snake_block])

        # Update the snake
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        draw_snake(snake_block, snake_list)
        display_score(length_of_snake - 1)

        pygame.display.update()

        # Control the game speed
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Run the game loop
game_loop()
