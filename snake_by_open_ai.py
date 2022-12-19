import pygame
import random

# Initialize pygame
pygame.init()

# Set the window size
window_size = (600, 600)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the title of the window
pygame.display.set_caption("Snake")

# Set the frame rate
frame_rate = pygame.time.Clock()

# Set the snake's initial position and velocity
x = 300
y = 300
velocity_x = 0
velocity_y = 0

# Set the snake's size
size = 20

# Set the snake's initial length
length = 1

# Set the initial position of the food
food_x = random.randint(0, window_size[0] - size)
food_y = random.randint(0, window_size[1] - size)

# Set the initial score
score = 0

# Set the initial game over flag
game_over = False

# Run the game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                velocity_x = 0
                velocity_y = -size
            elif event.key == pygame.K_DOWN:
                velocity_x = 0
                velocity_y = size
            elif event.key == pygame.K_LEFT:
                velocity_x = -size
                velocity_y = 0
            elif event.key == pygame.K_RIGHT:
                velocity_x = size
                velocity_y = 0

    # Update the snake's position
    x += velocity_x
    y += velocity_y

    # Check if the snake has eaten the food
    if x == food_x and y == food_y:
        # Increase the snake's length
        length += 1
        # Increase the score
        score += 1
        # Generate new food
        food_x = random.randint(0, window_size[0] - size)
        food_y = random.randint(0, window_size[1] - size)

    # Draw the snake and the food
    pygame.draw.rect(screen, (0, 255, 0), (x, y, size, size))
    pygame.draw.rect(screen, (255, 0, 0), (food_x, food_y, size, size))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    frame_rate.tick(10)

# Quit pygame
pygame.quit()
