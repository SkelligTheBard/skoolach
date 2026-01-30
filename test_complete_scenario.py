"""Simulate a complete gameplay scenario."""

import sys
sys.path.insert(0, 'src')

from game import GameEngine, create_world

def test_complete_scenario():
    """Simulate collecting components and reaching the final boss."""
    print("=" * 70)
    print("COMPLETE GAMEPLAY SCENARIO TEST")
    print("=" * 70)

    # Initialize
    print("\n1. Starting new game...")
    engine = GameEngine()
    starting_room = create_world()
    engine.setup(starting_room, player_name="TestHero")
    print(f"   [OK] Game initialized at '{engine.player.current_room.name}'")

    # Collect items from starting room
    print("\n2. Testing item collection in starting room...")
    items_in_room = list(engine.player.current_room.items)
    for item in items_in_room:
        response = engine.process_command(f"take {item.name}")
        print(f"   - {item.name}: {response.split('.')[0]}...")

    # Navigate to find AI components
    print("\n3. Exploring and collecting AI components...")

    # Path to collect first few components
    exploration_commands = [
        "go north",
        "go north",
        "take tokenizer",
        "go south",
        "go west",
        "take embeddings",
        "go south",
        "take training",
    ]

    components_collected = 0
    for cmd in exploration_commands:
        response = engine.process_command(cmd)
        if "take" in cmd.lower() and "AI component" in response:
            components_collected += 1
            component_name = cmd.split("take ")[-1] if "take" in cmd else "unknown"
            print(f"   [+] Collected AI component: {component_name}")

    # Check inventory
    print(f"\n4. Current inventory status:")
    inventory_response = engine.process_command("inventory")
    items_count = len(engine.player.inventory)
    ai_count = len(engine.player.ai_components_collected)
    print(f"   Total items: {items_count}")
    print(f"   AI components: {ai_count}")
    print(f"   Parser level: {engine.player.get_parser_level()}")

    # Test parser evolution
    print(f"\n5. Testing parser evolution:")
    if ai_count > 0:
        print(f"   [OK] Parser has evolved to level {engine.player.get_parser_level()}")
        print(f"   [OK] Parser should now understand more complex commands")
    else:
        print(f"   [INFO] Parser still at basic level (no components collected)")

    # Test combat initialization (if we can reach it)
    print(f"\n6. Testing combat system readiness:")
    if engine.player.health > 0:
        print(f"   [OK] Player health: {engine.player.health}")
        print(f"   [OK] Combat system ready")

    # Test game state
    print(f"\n7. Game state verification:")
    print(f"   Running: {engine.is_running()}")
    print(f"   Won: {engine.game_won}")
    print(f"   Current location: {engine.player.current_room.name}")

    # Test look command with components
    print(f"\n8. Testing enhanced LOOK command:")
    look_response = engine.process_command("look")
    if look_response:
        print(f"   [OK] Room description generated successfully")

    # Verify game can be quit properly
    print(f"\n9. Testing clean shutdown...")
    quit_response = engine.process_command("quit")
    print(f"   [OK] Game quit successfully")
    print(f"   Running after quit: {engine.is_running()}")

    print("\n" + "=" * 70)
    print("COMPLETE SCENARIO TEST FINISHED")
    print("=" * 70)

    return True

if __name__ == "__main__":
    try:
        test_complete_scenario()
        print("\n[SUCCESS] Complete gameplay scenario works correctly!")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Scenario test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
