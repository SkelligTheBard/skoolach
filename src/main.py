"""Main entry point for SKOOLACH with graphics."""

import sys
import os

# Check if pygame is available
try:
    import pygame
    GRAPHICS_AVAILABLE = True
except ImportError:
    GRAPHICS_AVAILABLE = False
    print("WARNING: pygame not installed. Graphics will not be available.")
    print("Install with: pip install pygame")
    print("Falling back to text-only mode...\n")

from game import GameEngine, create_world

if GRAPHICS_AVAILABLE:
    from graphics import GraphicsEngine


def main_with_graphics():
    """Main game loop with graphics."""
    # Create engines
    game_engine = GameEngine()
    graphics_engine = GraphicsEngine(
        width=1280,
        height=768,
        color_scheme='green',  # Classic terminal green
        use_effects=True
    )

    # Create world and setup game
    starting_room = create_world()
    game_engine.setup(starting_room, player_name="Coder")

    # Initialize graphics with starting room
    _update_graphics_room(game_engine, graphics_engine)

    # Display intro
    intro = game_engine.get_intro_text()
    graphics_engine.add_text(intro)
    graphics_engine.add_text("")
    graphics_engine.add_text(game_engine.player.current_room.get_description())
    graphics_engine.add_text("")
    graphics_engine.add_text("[TIP: Type HELP for commands. TAB=toggle camera, LEFT/RIGHT=rotate, UP/DOWN=scroll, DEL=clear text]")

    # Main game loop
    while game_engine.is_running():
        # Update status bar
        graphics_engine.set_status(game_engine.get_status_bar())

        # Handle input
        command, should_quit = graphics_engine.handle_input()

        if should_quit:
            break

        # Process command if one was entered
        if command:
            response = game_engine.process_command(command)

            if response:
                graphics_engine.add_text("")
                graphics_engine.add_text(response)

                # Update room visualization if player moved
                _update_graphics_room(game_engine, graphics_engine)

        # Update graphics
        delta_time = graphics_engine.render()
        graphics_engine.update(delta_time)

    # Cleanup
    graphics_engine.quit()

    # Show final message
    if game_engine.game_won:
        print("\n" + "=" * 70)
        print("CONGRATULATIONS! You've completed SKOOLACH!")
        print("You've learned the architecture of AI from the ground up.")
        print("=" * 70 + "\n")
    else:
        print("\n" + "=" * 70)
        print("Thanks for playing SKOOLACH!")
        print("=" * 70 + "\n")


def _update_graphics_room(game_engine, graphics_engine):
    """Update graphics engine with current room state."""
    if not game_engine.player or not game_engine.player.current_room:
        return

    room = game_engine.player.current_room

    # Get item names and AI component names
    item_names = [item.name for item in room.items]
    ai_component_names = [item.name for item in room.items if item.is_ai_component]

    # Update scene
    graphics_engine.set_current_room(
        room.name,
        item_names,
        ai_component_names
    )


def main_text_only():
    """Main game loop without graphics (text-only fallback)."""
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


def show_menu():
    """Show startup menu."""
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                         S K O O L A C H                          ║")
    print("║                  A Digital Archaeology Adventure                 ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()

    if GRAPHICS_AVAILABLE:
        print("Select mode:")
        print("  1. Play with retro vector graphics (recommended)")
        print("  2. Play text-only mode")
        print("  3. Quit")
        print()

        while True:
            choice = input("Enter choice (1-3): ").strip()

            if choice == "1":
                return "graphics"
            elif choice == "2":
                return "text"
            elif choice == "3":
                return "quit"
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    else:
        print("Graphics not available. Starting in text-only mode...")
        print("(Install pygame for graphics: pip install pygame)")
        print()
        input("Press Enter to continue...")
        return "text"


def main():
    """Main entry point."""
    mode = show_menu()

    if mode == "quit":
        print("\nGoodbye!")
        return

    print("\n" + "=" * 70)
    print("Starting SKOOLACH...")
    print("=" * 70 + "\n")

    if mode == "graphics":
        main_with_graphics()
    else:
        main_text_only()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
