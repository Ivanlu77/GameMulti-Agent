"""
Example: Create a simple game using GameAgent

This example demonstrates how to use the GameAgent system programmatically.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from GameAgent import GameOrchestrator, Config
from GameAgent.models import UserRequirement, GameGenre, GamePlatform


async def create_snake_game():
    """Create a classic snake game."""
    
    # Define requirements
    requirement = UserRequirement(
        description="""
        Create a classic Snake game with the following features:
        - Snake starts in the center of the screen
        - Food appears randomly on the screen
        - Snake grows longer when eating food
        - Game ends when snake hits wall or itself
        - Display score on screen
        - Snake speed increases as score goes up
        """,
        genre=GameGenre.ARCADE,
        platform=GamePlatform.PYGAME,
        target_audience="Casual gamers",
        additional_features=[
            "Colorful graphics",
            "Score display",
            "Game over screen with restart option"
        ]
    )
    
    # Create orchestrator and run
    config = Config.from_env()
    orchestrator = GameOrchestrator(config)
    
    game_code, review = await orchestrator.develop_game(requirement)
    
    print(f"\n✅ Game created successfully!")
    print(f"📊 Final score: {review.overall_score}/100")
    print(f"📁 Files: {[f.filename for f in game_code.files]}")
    
    return game_code, review


async def create_pong_game():
    """Create a Pong-style game."""
    
    requirement = UserRequirement(
        description="""
        Create a Pong game for two players:
        - Two paddles on left and right sides
        - Ball bounces between paddles
        - Score points when opponent misses
        - First to 5 points wins
        - Controls: W/S for left paddle, Up/Down for right paddle
        """,
        genre=GameGenre.ARCADE,
        platform=GamePlatform.PYGAME,
        additional_features=["Two player mode", "Sound effects (beeps)"]
    )
    
    config = Config.from_env()
    orchestrator = GameOrchestrator(config)
    
    return await orchestrator.develop_game(requirement)


async def create_puzzle_game():
    """Create a number puzzle game."""
    
    requirement = UserRequirement(
        description="""
        Create a 15-puzzle sliding tile game:
        - 4x4 grid with numbered tiles 1-15 and one empty space
        - Click/arrow keys to slide tiles into empty space
        - Goal is to arrange tiles in order
        - Show move counter
        - Shuffle button to start new game
        """,
        genre=GameGenre.PUZZLE,
        platform=GamePlatform.PYGAME,
        target_audience="Puzzle lovers"
    )
    
    config = Config.from_env()
    orchestrator = GameOrchestrator(config)
    
    return await orchestrator.develop_game(requirement)


async def create_platformer():
    """Create a simple platformer."""
    
    requirement = UserRequirement(
        description="""
        Create a simple platformer game:
        - Player character that can run and jump
        - Multiple platforms to jump between
        - Collectible coins
        - A goal/flag to reach
        - Gravity and physics
        - 3 levels with increasing difficulty
        """,
        genre=GameGenre.PLATFORMER,
        platform=GamePlatform.PYGAME,
        additional_features=["Parallax background", "Coin counter"]
    )
    
    config = Config.from_env()
    orchestrator = GameOrchestrator(config)
    
    return await orchestrator.develop_game(requirement)


if __name__ == "__main__":
    # Run the example
    print("🎮 GameAgent Example - Creating a Snake Game\n")
    
    try:
        asyncio.run(create_snake_game())
    except ValueError as e:
        print(f"\n❌ Configuration error: {e}")
        print("   Please set OPENAI_API_KEY environment variable")
    except KeyboardInterrupt:
        print("\n\n👋 Development cancelled")

