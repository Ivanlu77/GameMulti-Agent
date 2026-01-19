"""
Example: Iterative Game Development

This example demonstrates the cumulative iteration system:
1. Original requirement stays constant
2. First iteration creates baseline design and code
3. Each subsequent iteration:
   - Uses original requirement
   - Builds upon baseline (iteration 1)
   - Incorporates ALL accumulated feedback

Key Features:
- Iteration history is saved after each iteration
- Can resume from a saved history
- Feedback accumulates across iterations
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

from GameAgent.orchestrator import GameOrchestrator, resume_development
from GameAgent.config import Config
from GameAgent.models import (
    UserRequirement,
    GameGenre,
    GamePlatform,
    IterationHistory
)

# Load environment variables
load_dotenv()


async def develop_new_game():
    """
    Start developing a new game from scratch.
    
    The iteration flow:
    
    Iteration 1:
        Original Requirement → Designer → Developer → Player → Reviewer
                                  ↓
                            (Creates Baseline)
    
    Iteration 2+:
        Original Requirement
              +
        Baseline Design/Code (from iter 1)
              +
        Accumulated Feedback (from all previous iters)
              ↓
        Designer → Developer → Player → Reviewer
    """
    print("=" * 60)
    print("🎮 GameAgent - Iterative Development Demo")
    print("=" * 60)
    
    # Create the orchestrator
    config = Config.from_env()
    config.max_iterations = 3  # Allow up to 3 iterations
    
    orchestrator = GameOrchestrator(config)
    orchestrator.use_visual_play = False  # Use static analysis for demo
    
    # Define the original requirement
    # This will NEVER change throughout all iterations
    requirement = UserRequirement(
        description="""
        Create a Space Shooter game where:
        - Player controls a spaceship at the bottom of the screen
        - Enemies come from the top and the player must shoot them
        - Player has 3 lives
        - Score increases for each enemy destroyed
        - Game gets progressively harder
        """,
        genre=GameGenre.ARCADE,
        platform=GamePlatform.PYGAME,
        target_audience="casual gamers",
        additional_features=[
            "Power-ups that appear randomly",
            "Boss enemy every 1000 points"
        ]
    )
    
    print(f"\n📝 Original Requirement:")
    print(f"   {requirement.description[:100]}...")
    print(f"\n🎯 Genre: {requirement.genre.value}")
    print(f"🖥️ Platform: {requirement.platform.value}")
    print()
    
    try:
        # Run the development pipeline
        game_code, review, history = await orchestrator.develop_game(requirement)
        
        # Display results
        print("\n" + "=" * 60)
        print("📊 Development Complete!")
        print("=" * 60)
        print(f"Total Iterations: {len(history.snapshots)}")
        print(f"Final Score: {review.overall_score}/100")
        print(f"Ready for Delivery: {'✅ Yes' if review.ready_for_delivery else '❌ No'}")
        
        # Show iteration history
        print("\n📜 Iteration History:")
        for snap in history.snapshots:
            print(f"\n  Iteration {snap.iteration}:")
            print(f"    - Design: {snap.design_document.title if snap.design_document else 'N/A'}")
            print(f"    - Bugs Found: {len(snap.bugs_found)}")
            print(f"    - Improvements: {len(snap.improvements_needed)}")
            if snap.review:
                print(f"    - Review Score: {snap.review.overall_score}/100")
        
        # Show accumulated feedback
        print("\n📋 Accumulated Feedback:")
        print(f"  - Total Bugs Addressed: {len(history.all_bugs)}")
        print(f"  - Total Improvements Made: {len(history.all_improvements)}")
        print(f"  - Player Suggestions Used: {len(history.all_suggestions)}")
        print(f"  - Issues Fixed: {len(history.fixed_issues)}")
        
        return history
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Stopped by user")
        return None


async def resume_from_history(history_path: str):
    """
    Resume development from a saved iteration history.
    
    This is useful when:
    - Development was interrupted
    - You want to continue improving a game
    - You want to try different iteration strategies
    """
    print("=" * 60)
    print("🔄 Resuming Development from History")
    print("=" * 60)
    
    # Load the history
    history = IterationHistory.load(history_path)
    
    print(f"\n📂 Loaded history from: {history_path}")
    print(f"   Original Requirement: {history.original_requirement.description[:50]}...")
    print(f"   Previous Iterations: {len(history.snapshots)}")
    print(f"   Pending Improvements: {len(history.all_improvements)}")
    
    # Resume development
    game_code, review, updated_history = await resume_development(history_path)
    
    print("\n✅ Development resumed and completed!")
    return updated_history


async def demonstrate_iteration_context():
    """
    Demonstrate how iteration context is built and used.
    """
    print("=" * 60)
    print("🔍 Iteration Context Demo")
    print("=" * 60)
    
    # Create a sample history
    from GameAgent.models import (
        IterationSnapshot,
        GameDesignDocument,
        GameCode,
        CodeFile,
        PlaySession,
        GameReview,
        GameMechanic,
        DifficultyLevel
    )
    
    requirement = UserRequirement(
        description="A puzzle game where you match colors",
        genre=GameGenre.PUZZLE
    )
    
    history = IterationHistory(original_requirement=requirement)
    
    # Simulate iteration 1
    snap1 = IterationSnapshot(
        iteration=1,
        design_document=GameDesignDocument(
            title="Color Match",
            genre=GameGenre.PUZZLE,
            concept="Match 3 colors in a row",
            mechanics=[GameMechanic(name="matching", description="Match colors", implementation_notes="")],
            controls={"CLICK": "Select tile"},
            win_conditions=["Clear all tiles"],
            lose_conditions=["No moves left"],
            difficulty=DifficultyLevel.EASY
        ),
        game_code=GameCode(
            files=[CodeFile(filename="main.py", content="# Game code here")],
            main_file="main.py"
        ),
        play_session=PlaySession(
            session_id="test1",
            duration_seconds=30,
            bugs_found=["Tiles don't animate smoothly", "Score doesn't update"],
            suggestions=["Add combo bonuses", "Add sound effects"]
        ),
        review=GameReview(
            overall_score=65,
            must_fix=["Fix score display", "Add game over screen"],
            should_fix=["Improve animations"],
            strengths=["Fun concept"],
            weaknesses=["Missing polish"],
            summary="Good start but needs work"
        ),
        bugs_found=["Tiles don't animate smoothly", "Score doesn't update"],
        player_suggestions=["Add combo bonuses", "Add sound effects"],
        improvements_needed=["Fix score display", "Add game over screen", "Improve animations"]
    )
    
    history.add_iteration(snap1)
    
    # Show the context that would be used for iteration 2
    context = history.get_iteration_context()
    
    print("\n📌 Original Requirement (never changes):")
    print(f"   {context['original_requirement'].description}")
    
    print("\n🏗️ Baseline Design (from iteration 1):")
    print(f"   Title: {context['baseline_design'].title}")
    print(f"   Concept: {context['baseline_design'].concept}")
    
    print("\n🐛 Pending Bugs to Fix:")
    for bug in context['pending_bugs']:
        print(f"   - {bug}")
    
    print("\n📈 Pending Improvements:")
    for imp in context['pending_improvements']:
        print(f"   - {imp}")
    
    print("\n💡 Player Suggestions:")
    for sug in context['suggestions']:
        print(f"   - {sug}")
    
    print("\n✅ Fixed Issues (will not be reverted):")
    for fix in context['fixed_issues']:
        print(f"   - {fix}")
    
    print("\n" + "=" * 60)
    print("In iteration 2, the Designer and Developer will receive:")
    print("  1. The ORIGINAL requirement (core concept stays same)")
    print("  2. The BASELINE design/code (to build upon)")
    print("  3. ALL accumulated feedback (to address)")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--resume" and len(sys.argv) > 2:
            asyncio.run(resume_from_history(sys.argv[2]))
        elif sys.argv[1] == "--demo":
            asyncio.run(demonstrate_iteration_context())
        else:
            print("Usage:")
            print("  python iterative_development.py           # Start new game")
            print("  python iterative_development.py --resume <path>  # Resume from history")
            print("  python iterative_development.py --demo    # Show iteration context demo")
    else:
        asyncio.run(develop_new_game())
