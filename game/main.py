import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 36)

# Load assets
background_image = pygame.image.load("background.jpeg")  # Replace with your image
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
player_image = pygame.image.load("player.jpeg")  # Replace with your player image
player_image = pygame.transform.scale(player_image, (50, 50))
enemy_image = pygame.image.load("enemy.jpeg")  # Replace with your enemy image
enemy_image = pygame.transform.scale(enemy_image, (50, 50))

# Player settings
player_size = 50
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * player_size]
player_speed = 7

# Enemy settings
enemy_size = 50
enemy_list = []
enemy_speed = 5
ENEMY_SPAWN_RATE = 20  # Higher is slower spawn rate

# Function to drop enemies
def drop_enemies(enemy_list):
    if random.randint(0, ENEMY_SPAWN_RATE) < 1:
        x_pos = random.randint(0, SCREEN_WIDTH - enemy_size)
        enemy_list.append([x_pos, 0])

# Function to move enemies
def move_enemies(enemy_list):
    for enemy in enemy_list:
        enemy[1] += enemy_speed
        if enemy[1] > SCREEN_HEIGHT:
            enemy_list.remove(enemy)

# Function to detect collision
def detect_collision(player_pos, enemy_pos):
    px, py = player_pos
    ex, ey = enemy_pos
    return (ex < px < ex + enemy_size or ex < px + player_size < ex + enemy_size) and (ey < py < ey + enemy_size or ey < py + player_size < ey + enemy_size)

# Function to draw a gradient background
def draw_gradient(screen, start_color, end_color):
    for i in range(SCREEN_HEIGHT):
        color = [
            start_color[j] + (end_color[j] - start_color[j]) * i // SCREEN_HEIGHT
            for j in range(3)
        ]
        pygame.draw.line(screen, color, (0, i), (SCREEN_WIDTH, i))

# Game loop
score = 0
running = True
while running:
    screen.blit(background_image, (0, 0))  # Draw the background image

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - player_size:
        player_pos[0] += player_speed

    # Enemy behavior
    drop_enemies(enemy_list)
    move_enemies(enemy_list)

    # Collision detection
    for enemy in enemy_list:
        if detect_collision(player_pos, enemy):
            running = False

    # Draw player
    screen.blit(player_image, (player_pos[0], player_pos[1]))

    # Draw enemies
    for enemy in enemy_list:
        screen.blit(enemy_image, (enemy[0], enemy[1]))

    # Update score
    score += 1
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

# Quit the game
pygame.quit()
sys.exit()
