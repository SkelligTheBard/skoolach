"""Test the darkness mechanic."""

import sys
sys.path.insert(0, 'src')

from game import GameEngine, create_world

def test_darkness():
    """Test that darkness mechanics work properly."""
    print("=" * 70)
    print("DARKNESS MECHANIC TEST")
    print("=" * 70)

    # Setup game
    engine = GameEngine()
    starting_room = create_world()
    engine.setup(starting_room, player_name="DarknessTester")

    print("\n1. Starting at Crash Site")
    print(f"   Flashlight on: {engine.player.flashlight_on}")

    # Take flashlight
    print("\n2. Taking flashlight...")
    response = engine.process_command("take flashlight")
    print(f"   Response: {response}")

    # Go to Dark Archives without turning on flashlight
    print("\n3. Going to Dark Archives WITHOUT using flashlight...")
    engine.process_command("go north")  # Memory Corridor
    response = engine.process_command("go west")  # Dark Archives
    print(f"   Response (first 150 chars): {response[:150]}...")
    is_dark = response.startswith("It's pitch black")
    print(f"   Can see? {not is_dark}")

    # Try to take item without light
    print("\n4. Trying to take Training Data without light...")
    response = engine.process_command("take training")
    print(f"   Response: {response}")

    # Try to look without light
    print("\n5. Trying to look without light...")
    response = engine.process_command("look")
    print(f"   Response: {response}")

    # Use flashlight
    print("\n6. Using flashlight...")
    response = engine.process_command("use flashlight")
    print(f"   Flashlight on: {engine.player.flashlight_on}")
    print(f"   Response (first 200 chars): {response[:200]}...")

    # Try to look with light
    print("\n7. Looking around WITH light...")
    response = engine.process_command("look")
    print(f"   Can see description: {'shelves' in response.lower()}")
    print(f"   Can see items: {'training data' in response.lower()}")

    # Try to take item with light
    print("\n8. Taking Training Data WITH light...")
    response = engine.process_command("take training")
    print(f"   Success: {'take the' in response.lower()}")

    # Turn off flashlight
    print("\n9. Turning OFF flashlight...")
    response = engine.process_command("use flashlight")
    print(f"   Flashlight on: {engine.player.flashlight_on}")
    print(f"   Response: {response}")

    # Try to look again without light
    print("\n10. Looking without light again...")
    response = engine.process_command("look")
    is_dark_again = response.startswith("It's pitch black")
    print(f"   Dark again: {is_dark_again}")

    print("\n" + "=" * 70)
    print("DARKNESS MECHANIC TEST COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    test_darkness()
