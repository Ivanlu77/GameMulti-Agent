import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Infinite Serpent')

# Colors
BACKGROUND_COLOR = (15, 12, 41)
SNAKE_COLOR = (163, 217, 255)
ITEM_COLOR = (255, 255, 210)
OBSTACLE_COLOR = (84, 56, 100)
TEXT_COLOR = (255, 255, 255)

# Game settings
FPS = 60
clock = pygame.time.Clock()

snake_pos = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
snake_direction = 'UP'
snake_speed = 10
change_to = snake_direction

item_pos = [random.randrange(1, (SCREEN_WIDTH // 10)) * 10, random.randrange(1, (SCREEN_HEIGHT // 10)) * 10]
item_spawn = True

obstacles = []
for _ in range(10):  # Starting with 10 obstacles
    obstacles.append([random.randrange(1, (SCREEN_WIDTH // 10)) * 10, random.randrange(1, (SCREEN_HEIGHT // 10)) * 10])

score = 0

# Fonts
font = pygame.font.SysFont('arial', 35)

def show_score(choice, color, font, size):
    score_surface = font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (SCREEN_WIDTH / 10, 15)
    else:
        score_rect.midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.25)
    screen.blit(score_surface, score_rect)

def game_over():
    my_font = pygame.font.SysFont('arial', 50)
    GO_surface = my_font.render('Your Score is : ' + str(score), True, TEXT_COLOR)
    GO_rect = GO_surface.get_rect()
    GO_rect.midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    screen.fill(BACKGROUND_COLOR)
    screen.blit(GO_surface, GO_rect)
    show_score(0, TEXT_COLOR, 'times', 20)
    pygame.display.flip()
    # Wait 3 seconds then quit
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(screen, OBSTACLE_COLOR, pygame.Rect(obs[0], obs[1], 10, 10))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and change_to != 'DOWN':
                change_to = 'UP'
            if event.key == pygame.K_DOWN and change_to != 'UP':
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT and change_to != 'RIGHT':
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT and change_to != 'LEFT':
                change_to = 'RIGHT'

    # Validate direction
    if change_to == 'UP' and snake_direction != 'DOWN':
        snake_direction = 'UP'
    if change_to == 'DOWN' and snake_direction != 'UP':
        snake_direction = 'DOWN'
    if change_to == 'LEFT' and snake_direction != 'RIGHT':
        snake_direction = 'LEFT'
    if change_to == 'RIGHT' and snake_direction != 'LEFT':
        snake_direction = 'RIGHT'

    if snake_direction == 'UP':
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] - snake_speed)
    if snake_direction == 'DOWN':
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] + snake_speed)
    if snake_direction == 'LEFT':
        snake_pos[0] = (snake_pos[0][0] - snake_speed, snake_pos[0][1])
    if snake_direction == 'RIGHT':
        snake_pos[0] = (snake_pos[0][0] + snake_speed, snake_pos[0][1])

    # Snake body mechanics
    snake_pos.insert(0, list(snake_pos[0]))
    if snake_pos[0][0] == item_pos[0] and snake_pos[0][1] == item_pos[1]:
        score += 1
        item_spawn = False
    else:
        snake_pos.pop()

    if not item_spawn:
        item_pos = [random.randrange(1, (SCREEN_WIDTH // 10)) * 10, random.randrange(1, (SCREEN_HEIGHT // 10)) * 10]
    item_spawn = True

    screen.fill(BACKGROUND_COLOR)

    for pos in snake_pos:
        pygame.draw.rect(screen, SNAKE_COLOR, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(screen, ITEM_COLOR, pygame.Rect(item_pos[0], item_pos[1], 10, 10))

    # Check for collisions
    if snake_pos[0] in snake_pos[1:]:
        game_over()

    for obs in obstacles:
        if snake_pos[0][0] == obs[0] and snake_pos[0][1] == obs[1]:
            game_over()

    draw_obstacles(obstacles)

    show_score(1, TEXT_COLOR, font, 20)
    pygame.display.update()
    clock.tick(FPS)