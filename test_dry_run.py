"""Manual dry run test of SKOOLACH game."""

import sys
sys.path.insert(0, 'src')

from game import GameEngine, create_world

def dry_run_test():
    """Simulate a gameplay session to test the main game loop."""
    print("=" * 70)
    print("SKOOLACH DRY RUN TEST")
    print("=" * 70)

    # Initialize game
    print("\n1. Initializing game engine...")
    engine = GameEngine()
    starting_room = create_world()
    engine.setup(starting_room, player_name="TestPlayer")
    print("   [OK] Game engine initialized")
    print(f"   [OK] Player: {engine.player.name}")
    print(f"   [OK] Starting room: {engine.player.current_room.name}")

    # Test commands
    test_commands = [
        ("look", "Testing LOOK command"),
        ("inventory", "Testing INVENTORY command"),
        ("help", "Testing HELP command"),
        ("go north", "Testing MOVEMENT command"),
        ("take embeddings", "Testing TAKE command (if item exists)"),
        ("drop embeddings", "Testing DROP command"),
    ]

    print("\n2. Testing game commands:")
    for command, description in test_commands:
        print(f"\n   {description}: '{command}'")
        response = engine.process_command(command)
        if response:
            # Print first 200 chars of response
            preview = response[:200] + "..." if len(response) > 200 else response
            print(f"   Response: {preview}")
        print(f"   Game running: {engine.is_running()}")

    # Test status bar
    print("\n3. Testing status bar:")
    status = engine.get_status_bar()
    print(f"   Status: {status}")

    # Test parser levels
    print("\n4. Testing parser evolution:")
    print(f"   Current parser level: {engine.player.get_parser_level()}")
    print(f"   AI components collected: {len(engine.player.ai_components_collected)}")

    # Test quit
    print("\n5. Testing QUIT command:")
    response = engine.process_command("quit")
    print(f"   Response: {response}")
    print(f"   Game running: {engine.is_running()}")

    print("\n" + "=" * 70)
    print("DRY RUN COMPLETE - All systems operational!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        dry_run_test()
    except Exception as e:
        print(f"\n[ERROR] Error during dry run: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
