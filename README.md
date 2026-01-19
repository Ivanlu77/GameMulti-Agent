# 🎮 GameAgent - Multi-Agent Game Development System

A multi-agent game development system that automatically designs, develops, tests, and delivers complete games based on your requirements.

**[中文文档](README_zh.md)**

## ✨ Features

- **🎨 Designer Agent** - Transforms your ideas into detailed game design documents
- **💻 Developer Agent** - Writes complete, runnable game code
- **🎮 Player Agent** - Automatically tests games to find bugs and issues
- **📋 Reviewer Agent** - Evaluates game quality and decides if improvements are needed
- **🔄 Auto-Iteration** - Automatically fixes issues until the game meets delivery standards

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Requirements                        │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Orchestrator                               │
│         Coordinates all Agents, manages workflow             │
└────┬──────────────┬──────────────┬──────────────┬───────────┘
     ▼              ▼              ▼              ▼
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│Designer │──▶│Developer│──▶│ Player  │──▶│Reviewer │
│ Agent   │   │ Agent   │   │ Agent   │   │ Agent   │
└─────────┘   └─────────┘   └─────────┘   └─────────┘
                          │
                          ▼
              ┌───────────────────┐
              │  Perfect Game     │
              │    Delivered      │
              └───────────────────┘
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set API Key

```bash
# Windows PowerShell
$env:OPENAI_API_KEY = "your-api-key-here"

# Windows CMD
set OPENAI_API_KEY=your-api-key-here

# Linux/Mac
export OPENAI_API_KEY="your-api-key-here"
```

### 3. Run

```bash
# Interactive game creation
python main.py create

# Run demo
python main.py demo

# Check system configuration
python main.py check

# View all agents info
python main.py agents
```

## 📖 Usage

### Command Line Mode

```bash
# Interactive mode - System will ask what game you want
python main.py create

# Specify parameters directly
python main.py create --desc "A snake game" --genre arcade --platform pygame
```

### Programming Mode

```python
import asyncio
from GameAgent import GameOrchestrator, Config
from GameAgent.models import UserRequirement, GameGenre, GamePlatform

async def create_my_game():
    # Define game requirements
    requirement = UserRequirement(
        description="Create a snake game where the snake grows when eating food, game over when hitting wall or itself",
        genre=GameGenre.ARCADE,
        platform=GamePlatform.PYGAME,
        additional_features=["Score display", "Speed increase"]
    )
    
    # Create orchestrator and run
    config = Config.from_env()
    orchestrator = GameOrchestrator(config)
    
    game_code, review = await orchestrator.develop_game(requirement)
    
    print(f"Game created! Score: {review.overall_score}/100")
    return game_code, review

# Run
asyncio.run(create_my_game())
```

## 🎯 Supported Game Types

| Type | Description | Examples |
|------|-------------|----------|
| `arcade` | Arcade games | Snake, Breakout, Space Invaders |
| `puzzle` | Puzzle games | Tetris, Sudoku, Match-3 |
| `platformer` | Platform games | Mario-style games |
| `rpg` | Role-playing | Simple turn-based combat |
| `strategy` | Strategy games | Tower defense, Simple RTS |
| `card` | Card games | Blackjack, Poker |
| `simulation` | Simulation games | Simple business simulation |
| `adventure` | Adventure games | Text adventures |

## 🖥️ Supported Platforms

| Platform | Description |
|----------|-------------|
| `pygame` | Python Pygame 2D games (Recommended) |
| `web` | HTML5 Canvas web games |
| `terminal` | Terminal/Console games |

## 📁 Project Structure

```
GameAgent/
├── GameAgent/              # Core package
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── models.py          # Data models
│   ├── orchestrator.py    # Multi-Agent orchestrator
│   └── agents/            # AI Agents
│       ├── base.py        # Agent base class
│       ├── designer.py    # Designer Agent
│       ├── developer.py   # Developer Agent
│       ├── player.py      # Player/Tester Agent
│       └── reviewer.py    # Reviewer Agent
├── examples/              # Example code
│   ├── simple_game.py
│   └── custom_agents.py
├── games/                 # Generated games output directory
├── main.py               # Main entry point
├── requirements.txt      # Dependencies
└── README.md
```

## ⚙️ Configuration Options

Configure the system via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `MAX_ITERATIONS` | Maximum iterations | 10 |
| `DEBUG_MODE` | Debug mode | false |
| `OUTPUT_DIR` | Output directory | ./games |

## 🔧 Custom Agent Configuration

```python
from GameAgent.config import AgentConfig, Config

config = Config.from_env()

# More creative designer
config.designer_config = AgentConfig(
    model="gpt-4-turbo-preview",
    temperature=0.9,  # Higher creativity
    max_tokens=4096
)

# More precise developer
config.developer_config = AgentConfig(
    model="gpt-4-turbo-preview",
    temperature=0.3,  # Lower randomness
    max_tokens=8192
)
```

## 📝 Example Game Descriptions

### Snake Game
```
Create a classic snake game:
- Snake starts from the center of the screen
- Food appears randomly on the screen
- Eating food makes the snake longer and increases score
- Game over when hitting wall or itself
- Display current score
- Snake speed increases as score goes up
```

### Pong Two-Player
```
Create a two-player Pong game:
- Each side has a paddle
- Ball bounces between the two paddles
- Missing the ball gives opponent a point
- First to 5 points wins
- Controls: W/S for left side, Up/Down arrows for right side
```

### Tetris
```
Create a Tetris game:
- 7 different shaped blocks fall from the top
- Player can rotate and move blocks
- Completing a row clears it and scores points
- Game over when blocks reach the top
- Show next block preview
- Falling speed increases as score goes up
```

## 🤝 Workflow

1. **Requirements Analysis** - You describe the game you want
2. **Design Phase** - Designer Agent creates game design document
3. **Development Phase** - Developer Agent writes complete code
4. **Testing Phase** - Player Agent simulates playing and finds bugs
5. **Review Phase** - Reviewer Agent evaluates game quality
6. **Iterative Improvement** - Automatically returns to fix issues if not meeting standards
7. **Delivery** - Automatically delivered to games directory when score reaches 75+

## 📄 License

MIT License

---

**Made with ❤️ by GameAgent Team**
