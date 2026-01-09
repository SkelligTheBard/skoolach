"""Tests for the room system."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game.room import Room
from game.item import Item


def test_room_creation():
    """Test basic room creation."""
    room = Room("Test Room", "A test room", "Test Room (short)")

    assert room.name == "Test Room"
    assert room.description == "A test room"
    assert room.short_desc == "Test Room (short)"
    assert not room.visited

    print("[PASS]Room creation tests passed")


def test_room_exits():
    """Test room exits and connections."""
    room1 = Room("Room 1", "First room")
    room2 = Room("Room 2", "Second room")
    room3 = Room("Room 3", "Third room")

    # Add exits
    room1.add_exit("north", room2)
    room1.add_exit("east", room3)

    # Check exits exist
    assert "north" in room1.exits
    assert "east" in room1.exits
    assert "south" not in room1.exits

    # Check exit destinations
    assert room1.get_exit("north") == room2
    assert room1.get_exit("east") == room3

    print("[PASS]Room exits tests passed")


def test_room_locked_exits():
    """Test locked exits requiring items."""
    room1 = Room("Room 1", "First room")
    room2 = Room("Room 2", "Locked room")

    # Add locked exit
    room1.add_exit("north", room2, locked=True, required_item="Golden Key")

    # Test without key
    can_go, msg = room1.can_go("north", [])
    assert not can_go
    assert "Golden Key" in msg

    # Test with key
    key = Item("Golden Key", "A golden key")
    can_go, msg = room1.can_go("north", [key])
    assert can_go

    print("[PASS]Locked exits tests passed")


def test_room_items():
    """Test items in rooms."""
    room = Room("Test Room", "A room with items")

    # Add items
    item1 = Item("key", "A brass key", keywords=["key", "brass"])
    item2 = Item("book", "An old book", keywords=["book", "old"])

    room.add_item(item1)
    room.add_item(item2)

    assert len(room.items) == 2

    # Test finding items
    assert room.get_item("key") == item1
    assert room.get_item("book") == item2
    assert room.get_item("sword") is None

    # Test removing items
    room.remove_item(item1)
    assert len(room.items) == 1
    assert room.get_item("key") is None

    print("[PASS]Room items tests passed")


def test_room_description():
    """Test room descriptions."""
    room = Room("Test Room", "First time description", "Been here before")

    # First visit
    desc = room.get_description()
    assert "First time description" in desc
    assert room.visited

    # Second visit
    desc = room.get_description()
    assert "Been here before" in desc

    print("[PASS]Room description tests passed")


def test_room_description_with_items_and_exits():
    """Test room description includes items and exits."""
    room = Room("Test Room", "A room")
    room2 = Room("Other Room", "Another room")

    # Add items and exits
    item = Item("key", "A key")
    room.add_item(item)
    room.add_exit("north", room2)

    desc = room.get_description()

    # Check items are mentioned
    assert "key" in desc.lower()

    # Check exits are mentioned
    assert "north" in desc.lower()

    print("[PASS]Room description with items/exits tests passed")


if __name__ == "__main__":
    test_room_creation()
    test_room_exits()
    test_room_locked_exits()
    test_room_items()
    test_room_description()
    test_room_description_with_items_and_exits()
    print("\n[SUCCESS]All room tests passed!")
