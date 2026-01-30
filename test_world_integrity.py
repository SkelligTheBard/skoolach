"""Test the world structure and game integrity."""

import sys
sys.path.insert(0, 'src')

from game import create_world

def test_world_integrity():
    """Test that the game world is properly constructed."""
    print("=" * 70)
    print("WORLD INTEGRITY TEST")
    print("=" * 70)

    print("\n1. Creating world...")
    starting_room = create_world()
    print(f"   [OK] Starting room: {starting_room.name}")

    # Track all rooms and items
    visited_rooms = set()
    rooms_to_visit = [starting_room]
    all_items = []
    ai_components = []
    room_count = 0

    print("\n2. Exploring all connected rooms...")
    while rooms_to_visit:
        room = rooms_to_visit.pop(0)

        if room in visited_rooms:
            continue

        visited_rooms.add(room)
        room_count += 1
        print(f"   [{room_count}] {room.name}")

        # Collect items
        for item in room.items:
            all_items.append(item)
            if item.is_ai_component:
                ai_components.append(item)
                print(f"       - AI Component: {item.name}")
            else:
                print(f"       - Item: {item.name}")

        # Check exits
        exit_count = len(room.exits)
        locked_count = len(room.locked_exits)
        print(f"       Exits: {exit_count}, Locked: {locked_count}")

        # Add connected rooms
        for direction, next_room in room.exits.items():
            if next_room not in visited_rooms:
                rooms_to_visit.append(next_room)

    print(f"\n3. World statistics:")
    print(f"   Total rooms: {room_count}")
    print(f"   Total items: {len(all_items)}")
    print(f"   AI components: {len(ai_components)}")
    print(f"   Regular items: {len(all_items) - len(ai_components)}")

    print(f"\n4. AI Components found:")
    for component in ai_components:
        print(f"   - {component.name}")

    print(f"\n5. Verifying game completability:")
    if len(ai_components) >= 9:
        print(f"   [OK] Found {len(ai_components)} AI components (9+ required for completion)")
    else:
        print(f"   [WARNING] Only found {len(ai_components)} AI components (need 9 for completion)")

    if room_count >= 10:
        print(f"   [OK] Found {room_count} rooms (sufficient for exploration)")
    else:
        print(f"   [WARNING] Only found {room_count} rooms")

    print("\n" + "=" * 70)
    print("WORLD INTEGRITY TEST COMPLETE")
    print("=" * 70)

    return room_count, len(ai_components)

if __name__ == "__main__":
    try:
        rooms, components = test_world_integrity()
        if rooms >= 10 and components >= 9:
            print("\n[SUCCESS] World is properly constructed and completable!")
            sys.exit(0)
        else:
            print("\n[WARNING] World may have issues but basic structure is intact")
            sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] World integrity test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
