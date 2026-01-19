import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Snake settings
snake_pos = [[100, 50], [90, 50], [80, 50]]
snake_speed = [10, 0]
snake_size = 10

# Food
food_pos = [random.randrange(1, (SCREEN_WIDTH//10)) * 10,
            random.randrange(1, (SCREEN_HEIGHT//10)) * 10]
food_spawn = True

# Score
score = 0

# Main menu
def main_menu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu = False
        
        screen.fill(BLACK)
        font = pygame.font.SysFont('arial', 35)
        text = font.render('Press SPACE to start', True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(FPS)

# Game over
def game_over():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # Restart game
        
        screen.fill(BLACK)
        font = pygame.font.SysFont('arial', 35)
        text = font.render(f'Game Over! Your Score: {score}', True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(text, text_rect)
        
        restart_text = font.render('Press SPACE to restart', True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
        screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        clock.tick(FPS)

# Main game loop
def game_loop():
    global snake_pos, food_pos, food_spawn, score, snake_speed

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_speed[1] == 0:
                    snake_speed = [0, -10]
                elif event.key == pygame.K_DOWN and snake_speed[1] == 0:
                    snake_speed = [0, 10]
                elif event.key == pygame.K_LEFT and snake_speed[0] == 0:
                    snake_speed = [-10, 0]
                elif event.key == pygame.K_RIGHT and snake_speed[0] == 0:
                    snake_speed = [10, 0]

        # Snake movement
        snake_pos.insert(0, list(map(lambda x, y: x + y, snake_pos[0], snake_speed)))
        if snake_pos[0] in snake_pos[1:]:
            game_over()
            return  # Game over
        if snake_pos[0][0] < 0 or snake_pos[0][0] > SCREEN_WIDTH-snake_size or snake_pos[0][1] < 0 or snake_pos[0][1] > SCREEN_HEIGHT-snake_size:
            game_over()
            return  # Game over

        # Food collision
        if snake_pos[0] == food_pos:
            score += 1
            food_spawn = False
        else:
            snake_pos.pop()

        # Food spawn
        if not food_spawn:
            food_pos = [random.randrange(1, (SCREEN_WIDTH//10)) * 10,
                        random.randrange(1, (SCREEN_HEIGHT//10)) * 10]
        food_spawn = True

        # Drawing
        screen.fill(BLACK)
        for pos in snake_pos:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], snake_size, snake_size))
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], snake_size, snake_size))

        # Display score
        score_text = pygame.font.SysFont('arial', 20).render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, [0, 0])

        pygame.display.flip()
        clock.tick(FPS)

# Game start
main_menu()
game_loop()