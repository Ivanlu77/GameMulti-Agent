"""
GameAgent - Multi-Agent Game Development System

Main entry point for the application.

Run modes:
    python main.py create       # Interactive game creation
    python main.py create --visual  # With visual Player (actually plays the game!)
    python main.py demo         # Run demo
    python main.py resume       # Resume from saved history
    python main.py check        # Check configuration
"""

import asyncio
import sys
from pathlib import Path

# Add package to path
sys.path.insert(0, str(Path(__file__).parent))

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from GameAgent import GameOrchestrator, Config
from GameAgent.models import UserRequirement, GameGenre, GamePlatform, IterationHistory

app = typer.Typer(
    name="gameagent",
    help="Multi-Agent Game Development System - AI agents design, develop, test, and deliver games!"
)
console = Console()


def show_banner():
    """Display the application banner."""
    banner = """
    +===========================================================+
    |                                                           |
    |   GameAgent - Multi-Agent Game Development System         |
    |                                                           |
    |   Designer -> Developer -> Player -> Reviewer -> Deliver  |
    |                                                           |
    +===========================================================+
    """
    console.print(banner, style="bold blue")


@app.command()
def create(
    description: str = typer.Option(None, "--desc", "-d", help="Game description"),
    genre: str = typer.Option(None, "--genre", "-g", help="Game genre"),
    platform: str = typer.Option("pygame", "--platform", "-p", help="Target platform"),
    interactive: bool = typer.Option(True, "--interactive", "-i", help="Interactive mode"),
    visual: bool = typer.Option(False, "--visual", "-v", help="Enable visual play mode (Player actually plays the game!)"),
    max_iter: int = typer.Option(3, "--max-iter", "-m", help="Maximum iterations")
):
    """Create a new game from your requirements."""
    show_banner()
    
    # Interactive mode
    if interactive and not description:
        console.print("\n[bold]Let's create your dream game![/bold]\n")
        
        description = Prompt.ask(
            "[cyan]Describe the game you want to create[/cyan]",
            default="A simple snake game where you eat food and grow longer"
        )
        
        genre_options = [g.value for g in GameGenre]
        console.print(f"\n[dim]Available genres: {', '.join(genre_options)}[/dim]")
        genre = Prompt.ask(
            "[cyan]What genre?[/cyan]",
            default="arcade"
        )
        
        platform_options = [p.value for p in GamePlatform]
        console.print(f"\n[dim]Available platforms: {', '.join(platform_options)}[/dim]")
        platform = Prompt.ask(
            "[cyan]Target platform?[/cyan]",
            default="pygame"
        )
        
        visual = Confirm.ask(
            "\n[cyan]Enable visual play mode? (Player will actually run and play the game)[/cyan]",
            default=False
        )
    
    if not description:
        console.print("[red]Error: Please provide a game description[/red]")
        raise typer.Exit(1)
    
    # Create requirement
    try:
        requirement = UserRequirement(
            description=description,
            genre=GameGenre(genre) if genre else None,
            platform=GamePlatform(platform)
        )
    except ValueError as e:
        console.print(f"[red]Error: Invalid option - {e}[/red]")
        raise typer.Exit(1)
    
    # Show what we're building
    console.print(Panel(
        f"[bold]Game Description:[/bold] {description}\n"
        f"[bold]Genre:[/bold] {genre or 'Auto-detect'}\n"
        f"[bold]Platform:[/bold] {platform}\n"
        f"[bold]Visual Play:[/bold] {'✅ Enabled' if visual else '❌ Disabled'}\n"
        f"[bold]Max Iterations:[/bold] {max_iter}",
        title="Your Game Request",
        border_style="green"
    ))
    
    if interactive:
        if not Confirm.ask("\n[cyan]Start development?[/cyan]", default=True):
            console.print("[yellow]Development cancelled.[/yellow]")
            raise typer.Exit(0)
    
    # Run the development pipeline
    try:
        config = Config.from_env()
        config.max_iterations = max_iter
        
        orchestrator = GameOrchestrator(config)
        orchestrator.use_visual_play = visual
        
        game_code, review, history = asyncio.run(orchestrator.develop_game(requirement))
        
        console.print("\n" + "=" * 60)
        console.print("[bold green]=== GAME DEVELOPMENT COMPLETE! ===[/bold green]")
        console.print("=" * 60)
        console.print(f"\n[bold]Final Score:[/bold] {review.overall_score}/100")
        console.print(f"[bold]Iterations:[/bold] {len(history.snapshots)}")
        console.print(f"[bold]Files Generated:[/bold] {len(game_code.files)}")
        console.print(f"[bold]Bugs Fixed:[/bold] {len(history.fixed_issues)}")
        console.print(f"[bold]Output Directory:[/bold] ./games/")
        
    except ValueError as e:
        console.print(f"\n[red]Configuration Error: {e}[/red]")
        console.print("[dim]Make sure to set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable[/dim]")
        raise typer.Exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Development interrupted by user.[/yellow]")
        raise typer.Exit(0)
    except Exception as e:
        console.print(f"\n[red]Error during development: {e}[/red]")
        if "--debug" in sys.argv:
            raise
        raise typer.Exit(1)


@app.command()
def demo(
    visual: bool = typer.Option(False, "--visual", "-v", help="Enable visual play mode")
):
    """Run a demo game development."""
    show_banner()
    
    console.print("\n[bold]Running Demo - Creating a Snake Game[/bold]\n")
    console.print(f"[dim]Visual play mode: {'Enabled' if visual else 'Disabled'}[/dim]\n")
    
    requirement = UserRequirement(
        description="A classic snake game where the player controls a snake that grows longer by eating food. The game ends when the snake hits the wall or itself.",
        genre=GameGenre.ARCADE,
        platform=GamePlatform.PYGAME,
        additional_features=["Score display", "Increasing speed"]
    )
    
    try:
        config = Config.from_env()
        config.max_iterations = 2  # Quick demo
        
        orchestrator = GameOrchestrator(config)
        orchestrator.use_visual_play = visual
        
        game_code, review, history = asyncio.run(orchestrator.develop_game(requirement))
        
        console.print(f"\n[bold green]Demo complete![/bold green]")
        console.print(f"  Score: {review.overall_score}/100")
        console.print(f"  Iterations: {len(history.snapshots)}")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted.[/yellow]")
    except Exception as e:
        console.print(f"[red]Demo failed: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def resume(
    history_path: str = typer.Argument(..., help="Path to iteration history JSON file"),
    visual: bool = typer.Option(False, "--visual", "-v", help="Enable visual play mode")
):
    """Resume development from a saved iteration history."""
    show_banner()
    
    history_file = Path(history_path)
    if not history_file.exists():
        console.print(f"[red]Error: History file not found: {history_path}[/red]")
        raise typer.Exit(1)
    
    try:
        # Load history
        history = IterationHistory.load(str(history_file))
        
        console.print(Panel(
            f"[bold]Original Requirement:[/bold]\n{history.original_requirement.description[:200]}...\n\n"
            f"[bold]Previous Iterations:[/bold] {len(history.snapshots)}\n"
            f"[bold]Pending Bugs:[/bold] {len(history.all_bugs)}\n"
            f"[bold]Pending Improvements:[/bold] {len(history.all_improvements)}",
            title="Resuming Development",
            border_style="yellow"
        ))
        
        if not Confirm.ask("\n[cyan]Continue development?[/cyan]", default=True):
            console.print("[yellow]Cancelled.[/yellow]")
            raise typer.Exit(0)
        
        config = Config.from_env()
        orchestrator = GameOrchestrator(config)
        orchestrator.use_visual_play = visual
        
        game_code, review, updated_history = asyncio.run(
            orchestrator.develop_game(history.original_requirement, resume_from=history)
        )
        
        console.print(f"\n[bold green]Development resumed and completed![/bold green]")
        console.print(f"  Final Score: {review.overall_score}/100")
        console.print(f"  Total Iterations: {len(updated_history.snapshots)}")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def check():
    """Check system configuration."""
    show_banner()
    
    console.print("\n[bold]Checking configuration...[/bold]\n")
    
    import os
    
    checks = [
        ("OPENAI_API_KEY", bool(os.getenv("OPENAI_API_KEY"))),
        ("ANTHROPIC_API_KEY", bool(os.getenv("ANTHROPIC_API_KEY"))),
    ]
    
    all_good = False
    for name, status in checks:
        icon = "[green][OK][/green]" if status else "[red][X][/red]"
        console.print(f"  {icon} {name}: {'Configured' if status else 'Not set'}")
        if status:
            all_good = True
    
    # Check dependencies
    console.print("\n[bold]Checking dependencies...[/bold]\n")
    
    deps = ["pygame", "langchain", "langchain_openai", "rich", "typer", "pydantic"]
    for dep in deps:
        try:
            __import__(dep.replace("-", "_"))
            console.print(f"  [green][OK][/green] {dep}")
        except ImportError:
            console.print(f"  [red][X][/red] {dep} - Not installed")
    
    if all_good:
        console.print("\n[green][OK] System is ready! Run 'python main.py create' to start.[/green]")
    else:
        console.print("\n[yellow][!] Please set at least one API key to continue.[/yellow]")
        console.print("[dim]  $env:OPENAI_API_KEY = 'your_key_here'[/dim]")


@app.command()
def agents():
    """Show information about the agents."""
    show_banner()
    
    agents_info = [
        ("[Designer Agent]", "Transforms your requirements into detailed Game Design Documents (GDD)", 
         ["Analyzes user requirements", "Designs game mechanics", "Specifies art and audio", "Plans levels and progression"]),
        
        ("[Developer Agent]", "Writes complete, working game code",
         ["Implements all mechanics", "Generates procedural assets", "Handles platform specifics", "Writes clean, documented code"]),
        
        ("[Player Agent]", "Tests games by simulating gameplay",
         ["Analyzes code for bugs", "Simulates player behavior", "Tests edge cases", "Evaluates fun factor"]),
        
        ("[Reviewer Agent]", "Reviews games and decides on delivery",
         ["Scores gameplay quality", "Identifies improvements", "Makes delivery decisions", "Generates reports"])
    ]
    
    for name, desc, tasks in agents_info:
        task_list = "\n".join([f"    - {t}" for t in tasks])
        console.print(Panel(
            f"[bold]{desc}[/bold]\n\n[dim]Tasks:[/dim]\n{task_list}",
            title=name,
            border_style="blue"
        ))
        console.print()


if __name__ == "__main__":
    app()

