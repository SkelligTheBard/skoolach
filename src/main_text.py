"""Main entry point for SKOOLACH text adventure game."""

import sys
from game import GameEngine, create_world


def main():
    """Main game loop."""
    # Create the game engine
    engine = GameEngine()

    # Create the world
    starting_room = create_world()

    # Set up the game
    engine.setup(starting_room, player_name="Coder")

    # Display intro
    print(engine.get_intro_text())
    print(engine.player.current_room.get_description())
    print()

    # Main game loop
    while engine.is_running():
        # Show status bar
        print(f"\n[{engine.get_status_bar()}]")

        # Get player input
        try:
            command = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGame interrupted. Thanks for playing!")
            break

        if not command:
            continue

        # Process command
        response = engine.process_command(command)

        if response:
            print(f"\n{response}")

    print("\n╔══════════════════════════════════════════════════════════════════╗")
    print("║                    Thanks for playing SKOOLACH!                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝\n")


if __name__ == "__main__":
    main()
