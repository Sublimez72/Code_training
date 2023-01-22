import pygame
import random

# Initialize Pygame
pygame.init()

# Set the screen size
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title and icon of the game window
pygame.display.set_caption("Snake Game")


# Set the colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Set the snake block size and initial position
block_size = 20
snake_x = 300
snake_y = 300

# Set the initial direction of the snake
snake_dir = "right"

# Set the initial snake length
snake_length = 1

snake_body = []
for i in range(snake_length):
    snake_body.append([snake_x, snake_y])
# Set the initial apple position
apple_x = random.randint(0, screen_width/block_size-1) * block_size
apple_y = random.randint(0, screen_height/block_size-1) * block_size


# Create a font object for displaying the score
font = pygame.font.Font(None, 30)

# Set the game over flag
game_over = False

clock = pygame.time.Clock()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake_dir != "right":
                snake_dir = "left"
            elif event.key == pygame.K_RIGHT and snake_dir != "left":
                snake_dir = "right"
            elif event.key == pygame.K_UP and snake_dir != "down":
                snake_dir = "up"
            elif event.key == pygame.K_DOWN and snake_dir != "up":
                snake_dir = "down"
    if snake_dir == "right":
        snake_x += block_size / 4
    elif snake_dir == "left":
        snake_x -= block_size / 4
    elif snake_dir == "up":
        snake_y -= block_size / 4
    elif snake_dir == "down":
        snake_y += block_size / 4

   # Check for collision with the borders
    if snake_x >= screen_width or snake_x < 0 or snake_y >= screen_height or snake_y < 0:
        game_over = True

    # Clear the screen
    screen.fill(black)

    # check if snake hit the apple
    if (snake_x-apple_x)**2 + (snake_y-apple_y)**2 <= (block_size/2)**2:
        # Increase the snake's length
        snake_length += 1
        # Randomize the apple's position
        apple_x = random.randint(0, screen_width/block_size-1) * block_size
        apple_y = random.randint(0, screen_height/block_size-1) * block_size
        # Add a new block to the snake's body
        snake_body.append([snake_x, snake_y])

    for i in range(len(snake_body) - 1, 0, -1):
        snake_body[i] = snake_body[i - 1][:]

    snake_body[0] = [snake_x, snake_y]

    for i in range(len(snake_body)):
        pygame.draw.rect(
            screen, white, [snake_body[i][0], snake_body[i][1], block_size, block_size])
    pygame.display.update()

    for i in range(1, len(snake_body)):
        if snake_x == snake_body[i][0] and snake_y == snake_body[i][1]:
            game_over = True

    # Draw the apple
    pygame.draw.rect(screen, red, [apple_x, apple_y, block_size, block_size])

    # Display the score
    score = font.render("Score: " + str(snake_length-1), True, white)
    screen.blit(score, (5, 5))

    # Update the screen
    clock.tick(60)
    pygame.display.update()

# Exit Pygame
pygame.quit()
