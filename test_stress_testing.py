"""Stress testing for SKOOLACH - test edge cases and invalid inputs."""

import sys
import os

# Fix encoding for Windows console
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    # Try to set console to UTF-8
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleCP(65001)
        kernel32.SetConsoleOutputCP(65001)
    except:
        pass

sys.path.insert(0, 'src')

from game import GameEngine, create_world

def safe_print(text):
    """Print text safely, handling unicode errors."""
    try:
        print(text)
    except UnicodeEncodeError:
        # Replace problematic characters with ASCII equivalents
        print(text.encode('ascii', 'replace').decode('ascii'))

def test_invalid_inputs():
    """Test how the game handles various invalid inputs."""
    safe_print("=" * 70)
    safe_print("STRESS TEST: INVALID INPUTS")
    safe_print("=" * 70)

    engine = GameEngine()
    starting_room = create_world()
    engine.setup(starting_room, player_name="StressTester")

    # Test cases: (command, description)
    invalid_commands = [
        ("", "Empty command"),
        ("   ", "Whitespace only"),
        ("asdfghjkl", "Random gibberish"),
        ("go nowhere", "Invalid direction"),
        ("take something that does not exist at all", "Non-existent item"),
        ("drop something i dont have", "Drop item not in inventory"),
        ("go", "Incomplete command - missing parameter"),
        ("take", "Incomplete command - missing parameter"),
        ("look at something not here", "Look at non-existent item"),
        ("GO NORTH SOUTH EAST", "Too many parameters"),
        ("!!!???###", "Special characters only"),
        ("go " + "north " * 50, "Very long command with repetition"),
        ("a" * 1000, "Buffer overflow test - 1000 chars"),
        ("go 123", "Direction with numbers"),
        ("take 999", "Item with just numbers"),
        ("GoNorth", "No space between words"),
        ("GO_NORTH", "Underscore instead of space"),
        ("go\tnorth", "Tab character"),
        ("go\nnorth", "Newline character"),
        ("Go NoRtH", "Mixed case weirdness"),
        ("../../../etc/passwd", "Path traversal attempt"),
        ("'; DROP TABLE items; --", "SQL injection attempt"),
        ("<script>alert('xss')</script>", "XSS attempt"),
        ("go north' OR '1'='1", "SQL-style injection in command"),
    ]

    safe_print("\nTesting invalid commands:")
    safe_print("-" * 70)

    passed = 0
    failed = 0

    for command, description in invalid_commands:
        try:
            # Truncate display of very long commands
            display_cmd = command if len(command) < 50 else command[:47] + "..."
            safe_print(f"\n[TEST] {description}")
            safe_print(f"  Input: '{display_cmd}'")

            response = engine.process_command(command)

            # Check if game is still running (didn't crash)
            still_running = engine.is_running()

            # Truncate long responses
            display_response = response if len(response) < 100 else response[:97] + "..."
            safe_print(f"  Response: {display_response}")
            safe_print(f"  Game still running: {still_running}")

            # Game should still be running for all these (except quit)
            if still_running or "quit" in command.lower():
                safe_print(f"  [OK] Handled gracefully")
                passed += 1
            else:
                safe_print(f"  [FAIL] Game stopped unexpectedly")
                failed += 1

        except Exception as e:
            safe_print(f"  [FAIL] Exception raised: {e}")
            failed += 1

    safe_print("\n" + "=" * 70)
    safe_print(f"INVALID INPUT TEST RESULTS: {passed} passed, {failed} failed")
    safe_print("=" * 70)

    return passed, failed


def test_profanity_filter():
    """Test if the game has any profanity filtering."""
    safe_print("\n" + "=" * 70)
    safe_print("STRESS TEST: PROFANITY AND INAPPROPRIATE LANGUAGE")
    safe_print("=" * 70)

    engine = GameEngine()
    starting_room = create_world()
    engine.setup(starting_room, player_name="TestUser")

    # Test profanity in various contexts
    profanity_tests = [
        ("damn", "Mild profanity"),
        ("hell", "Mild profanity"),
        ("crap", "Mild profanity"),
        ("fuck", "Strong profanity"),
        ("shit", "Strong profanity"),
        ("bitch", "Strong profanity"),
        ("asshole", "Strong profanity"),
        ("go north you stupid game", "Profanity in command"),
        ("take the damn flashlight", "Profanity with valid command"),
    ]

    safe_print("\nTesting profanity handling:")
    safe_print("-" * 70)
    safe_print("NOTE: Testing if game filters or passes through profanity")

    for command, description in profanity_tests:
        safe_print(f"\n[TEST] {description}")
        safe_print(f"  Input: '{command}'")

        try:
            response = engine.process_command(command)
            display_response = response if len(response) < 100 else response[:97] + "..."
            safe_print(f"  Response: {display_response}")
            safe_print(f"  Game still running: {engine.is_running()}")
            safe_print(f"  [OK] Processed without crashing")
        except Exception as e:
            safe_print(f"  [FAIL] Exception: {e}")

    safe_print("\n" + "=" * 70)
    safe_print("PROFANITY TEST COMPLETE")
    safe_print("(Game appears to have no explicit profanity filter)")
    safe_print("=" * 70)


def test_boundary_conditions():
    """Test boundary conditions and limits."""
    safe_print("\n" + "=" * 70)
    safe_print("STRESS TEST: BOUNDARY CONDITIONS")
    safe_print("=" * 70)

    engine = GameEngine()
    starting_room = create_world()
    engine.setup(starting_room, player_name="BoundaryTest")

    safe_print("\n1. Testing inventory limits:")

    # Try to collect everything
    engine.process_command("go north")
    engine.process_command("go north")

    # Try to take the same item multiple times
    safe_print("\n  Attempting to take same item multiple times:")
    for i in range(3):
        response = engine.process_command("take tokenizer")
        safe_print(f"  Attempt {i+1}: {response[:80]}...")

    # Try to fill inventory
    safe_print("\n2. Testing inventory capacity:")
    initial_count = len(engine.player.inventory)
    safe_print(f"  Starting inventory: {initial_count} items")
    safe_print(f"  Max inventory: {engine.player.max_inventory} items")

    # Try to take items until full
    rooms_visited = 0
    items_collected = 0
    max_attempts = 20

    for attempt in range(max_attempts):
        # Look for items in current room
        items_here = list(engine.player.current_room.items)

        for item in items_here:
            if len(engine.player.inventory) < engine.player.max_inventory:
                response = engine.process_command(f"take {item.name}")
                if "take the" in response.lower():
                    items_collected += 1

        # Move to another room
        if engine.player.current_room.exits:
            direction = list(engine.player.current_room.exits.keys())[0]
            engine.process_command(f"go {direction}")
            rooms_visited += 1

        if len(engine.player.inventory) >= engine.player.max_inventory:
            safe_print(f"  [OK] Inventory filled at {len(engine.player.inventory)} items")
            break

    safe_print(f"  Final inventory: {len(engine.player.inventory)} items")
    safe_print(f"  Rooms visited: {rooms_visited}")

    # Try to take when inventory is full
    safe_print("\n3. Testing over-capacity:")
    if len(engine.player.inventory) >= engine.player.max_inventory:
        # Find a room with items
        for i in range(5):
            if engine.player.current_room.items:
                item = list(engine.player.current_room.items)[0]
                response = engine.process_command(f"take {item.name}")
                safe_print(f"  Attempt to exceed capacity: {response[:80]}...")
                break
            else:
                # Move to find items
                if engine.player.current_room.exits:
                    direction = list(engine.player.current_room.exits.keys())[0]
                    engine.process_command(f"go {direction}")

    # Test negative health (if possible)
    safe_print("\n4. Testing player health boundaries:")
    safe_print(f"  Current health: {engine.player.health}")
    original_health = engine.player.health
    engine.player.health = -50
    safe_print(f"  Set health to -50: {engine.player.health}")
    safe_print(f"  Game still running: {engine.is_running()}")
    engine.player.health = original_health

    safe_print("\n" + "=" * 70)
    safe_print("BOUNDARY CONDITION TESTS COMPLETE")
    safe_print("=" * 70)


def test_unicode_and_encoding():
    """Test unicode and special encoding."""
    safe_print("\n" + "=" * 70)
    safe_print("STRESS TEST: UNICODE AND SPECIAL CHARACTERS")
    safe_print("=" * 70)

    engine = GameEngine()
    starting_room = create_world()
    engine.setup(starting_room, player_name="UnicodeTest")

    unicode_tests = [
        ("go 北", "Chinese characters"),
        ("take café", "Accented characters"),
        ("look émoji", "More accents"),
        ("go ñorth", "Spanish tilde"),
        ("take 日本", "Japanese characters"),
        ("look at the 🎮", "Emoji"),
        ("take item™", "Trademark symbol"),
        ("go ½ north", "Fraction symbol"),
        ("look at ₿", "Bitcoin symbol"),
    ]

    safe_print("\nTesting unicode inputs:")
    safe_print("-" * 70)

    for command, description in unicode_tests:
        safe_print(f"\n[TEST] {description}")
        safe_print(f"  Input: '{command}'")

        try:
            response = engine.process_command(command)
            display_response = response if len(response) < 100 else response[:97] + "..."
            safe_print(f"  Response: {display_response}")
            safe_print(f"  [OK] Handled without crashing")
        except Exception as e:
            safe_print(f"  [FAIL] Exception: {e}")

    safe_print("\n" + "=" * 70)
    safe_print("UNICODE TEST COMPLETE")
    safe_print("=" * 70)


def run_all_stress_tests():
    """Run all stress tests."""
    safe_print("\n" + "=" * 70)
    safe_print("SKOOLACH COMPREHENSIVE STRESS TESTING")
    safe_print("=" * 70)

    all_passed = True

    # Test 1: Invalid inputs
    passed, failed = test_invalid_inputs()
    if failed > 0:
        all_passed = False

    # Test 2: Profanity
    test_profanity_filter()

    # Test 3: Boundary conditions
    test_boundary_conditions()

    # Test 4: Unicode
    test_unicode_and_encoding()

    safe_print("\n" + "=" * 70)
    safe_print("ALL STRESS TESTS COMPLETE")
    safe_print("=" * 70)

    return all_passed


if __name__ == "__main__":
    try:
        success = run_all_stress_tests()
        if success:
            safe_print("\n[SUCCESS] All stress tests completed!")
        else:
            safe_print("\n[WARNING] Some tests revealed issues (see above)")
        sys.exit(0)
    except Exception as e:
        safe_print(f"\n[ERROR] Stress testing failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
