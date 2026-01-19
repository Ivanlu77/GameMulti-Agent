"""
Example: Using custom agent configurations

This example shows how to customize agent behavior.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from GameAgent import GameOrchestrator, Config
from GameAgent.config import AgentConfig
from GameAgent.models import UserRequirement, GameGenre, GamePlatform


async def create_with_custom_config():
    """Create a game with custom agent configurations."""
    
    # Create custom configuration
    config = Config.from_env()
    
    # Customize Designer agent - more creative
    config.designer_config = AgentConfig(
        model="gpt-4-turbo-preview",
        temperature=0.9,  # Higher creativity
        max_tokens=4096
    )
    
    # Customize Developer agent - more precise
    config.developer_config = AgentConfig(
        model="gpt-4-turbo-preview",
        temperature=0.3,  # Lower for more consistent code
        max_tokens=8192   # More tokens for complex games
    )
    
    # Allow more iterations for polishing
    config.max_iterations = 5
    
    # Create orchestrator with custom config
    orchestrator = GameOrchestrator(config)
    
    # Create a more complex game
    requirement = UserRequirement(
        description="""
        Create an RPG-lite dungeon crawler:
        - Player explores a procedurally generated dungeon
        - Turn-based combat with simple attack/defend
        - Find items and gold
        - Beat the boss on level 5
        - Simple stats: HP, Attack, Defense
        """,
        genre=GameGenre.RPG,
        platform=GamePlatform.PYGAME,
        target_audience="RPG enthusiasts"
    )
    
    game_code, review = await orchestrator.develop_game(requirement)
    
    print(f"\n✅ RPG created with score: {review.overall_score}/100")
    return game_code, review


async def create_terminal_game():
    """Create a terminal-based game."""
    
    config = Config.from_env()
    orchestrator = GameOrchestrator(config)
    
    requirement = UserRequirement(
        description="""
        Create a text-based adventure game:
        - Player explores rooms with text descriptions
        - Commands like 'go north', 'take item', 'use item'
        - Simple puzzle to solve
        - Multiple endings based on choices
        """,
        genre=GameGenre.ADVENTURE,
        platform=GamePlatform.TERMINAL
    )
    
    return await orchestrator.develop_game(requirement)


if __name__ == "__main__":
    print("🎮 Custom Configuration Example\n")
    
    try:
        asyncio.run(create_with_custom_config())
    except Exception as e:
        print(f"\n❌ Error: {e}")

