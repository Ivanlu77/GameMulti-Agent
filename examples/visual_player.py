"""
Example: Visual Player Agent

This example demonstrates how the Player Agent can:
1. Launch a game
2. Observe the game through screen capture
3. Analyze the game state using GPT-4o vision
4. Make decisions and control the game with keyboard/mouse

Requirements:
- OpenAI API key with GPT-4o access
- Install dependencies: pip install mss pyautogui pillow pywin32
"""

import asyncio
import os
from dotenv import load_dotenv

from GameAgent.agents.player import PlayerAgent
from GameAgent.config import AgentConfig
from GameAgent.models import (
    GameDesignDocument,
    GameCode,
    CodeFile,
    GameGenre,
    GamePlatform,
    DifficultyLevel,
    GameMechanic
)

# Load environment variables
load_dotenv()


# Example: A simple game for the Player to test
SIMPLE_GAME_CODE = '''
import pygame
import random
import sys

# Initialize
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Catch the Stars")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Game state
player_x = 400
player_y = 500
player_speed = 8
score = 0
game_over = False

# Stars
stars = []
star_spawn_timer = 0

def spawn_star():
    stars.append({
        'x': random.randint(20, 780),
        'y': -20,
        'speed': random.randint(3, 7)
    })

# Game loop
running = True
while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if game_over and event.key == pygame.K_SPACE:
                # Restart
                game_over = False
                score = 0
                stars.clear()
                player_x = 400
    
    if not game_over:
        # Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed
        
        # Keep player in bounds
        player_x = max(25, min(775, player_x))
        
        # Spawn stars
        star_spawn_timer += 1
        if star_spawn_timer > 30:
            spawn_star()
            star_spawn_timer = 0
        
        # Update stars
        for star in stars[:]:
            star['y'] += star['speed']
            
            # Check collision with player
            if abs(star['x'] - player_x) < 40 and abs(star['y'] - player_y) < 40:
                stars.remove(star)
                score += 10
            
            # Remove if off screen
            elif star['y'] > 620:
                stars.remove(star)
                game_over = True
    
    # Draw
    screen.fill((20, 20, 50))  # Dark blue background
    
    # Draw stars
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 0), (int(star['x']), int(star['y'])), 10)
    
    # Draw player
    pygame.draw.rect(screen, (0, 200, 255), (player_x - 25, player_y - 10, 50, 20))
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    # Game over screen
    if game_over:
        game_over_text = font.render("GAME OVER - Press SPACE to restart", True, (255, 0, 0))
        screen.blit(game_over_text, (200, 300))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
'''


async def main():
    """Run the visual player example."""
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY environment variable")
        return
    
    # Create game design document
    gdd = GameDesignDocument(
        title="Catch the Stars",
        genre=GameGenre.ARCADE,
        concept="A simple arcade game where you catch falling stars",
        mechanics=[
            GameMechanic(
                name="Movement",
                description="Player moves left and right to catch stars",
                implementation_notes="Arrow keys or A/D"
            ),
            GameMechanic(
                name="Catching",
                description="Catch stars to score points",
                implementation_notes="Collision detection"
            )
        ],
        controls={
            "LEFT": "Move left",
            "RIGHT": "Move right",
            "A": "Move left",
            "D": "Move right",
            "SPACE": "Restart game",
            "ESCAPE": "Quit"
        },
        win_conditions=["Score as high as possible"],
        lose_conditions=["Let a star fall off the bottom of the screen"],
        platform=GamePlatform.PYGAME,
        difficulty=DifficultyLevel.EASY
    )
    
    # Create game code
    game_code = GameCode(
        files=[
            CodeFile(
                filename="main.py",
                content=SIMPLE_GAME_CODE,
                language="python",
                description="Main game file"
            )
        ],
        main_file="main.py",
        dependencies=["pygame"]
    )
    
    # Create player agent
    config = AgentConfig(
        model="gpt-4o",
        temperature=0.3,
        max_tokens=2000
    )
    
    player = PlayerAgent(
        config=config,
        api_key=api_key,
        provider="openai",
        vision_model="gpt-4o",
        debug=True  # Save debug screenshots
    )
    
    # Configure play settings
    player.max_play_duration = 60  # Play for 60 seconds
    player.observation_interval = 1.5  # Observe every 1.5 seconds
    
    print("=" * 60)
    print("🎮 Visual Player Agent Demo")
    print("=" * 60)
    print(f"Game: {gdd.title}")
    print(f"Genre: {gdd.genre.value}")
    print(f"Duration: {player.max_play_duration}s")
    print()
    print("The Player Agent will:")
    print("1. Launch the game")
    print("2. Observe the screen using GPT-4o vision")
    print("3. Decide what actions to take")
    print("4. Control the game with keyboard inputs")
    print()
    print("Press Ctrl+C to stop early")
    print("=" * 60)
    
    try:
        # Run the visual player
        session = await player.process(
            {
                "game_code": game_code,
                "gdd": gdd,
                "use_vision": True  # Enable visual play!
            }
        )
        
        # Print results
        print()
        print("=" * 60)
        print("📊 Play Session Results")
        print("=" * 60)
        print(f"Duration: {session.duration_seconds:.1f} seconds")
        print(f"Completed: {session.completed}")
        print(f"Score: {session.score}")
        print(f"Fun Rating: {session.fun_rating}/10")
        print(f"Difficulty Rating: {session.difficulty_rating}/10")
        print()
        
        if session.bugs_found:
            print("🐛 Bugs Found:")
            for bug in session.bugs_found:
                print(f"  - {bug}")
        
        if session.suggestions:
            print("\n💡 Suggestions:")
            for suggestion in session.suggestions:
                print(f"  - {suggestion}")
        
        if session.observations:
            print("\n👀 Observations:")
            for obs in session.observations[:5]:
                print(f"  - {obs}")
                
    except KeyboardInterrupt:
        print("\n\nStopped by user")
    except Exception as e:
        print(f"\nError: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
