"""Tests for the player system."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game.player import Player
from game.item import Item, AIComponent
from game.room import Room


def test_player_inventory():
    """Test player inventory management."""
    player = Player("Tester")

    # Test empty inventory
    assert len(player.inventory) == 0

    # Test adding item
    item = Item("test key", "A test key")
    success, msg = player.take_item(item)
    assert success
    assert item in player.inventory
    assert len(player.inventory) == 1

    # Test dropping item
    success, msg = player.drop_item(item)
    assert success
    assert item not in player.inventory
    assert len(player.inventory) == 0

    print("[PASS]Inventory tests passed")


def test_player_ai_components():
    """Test AI component tracking."""
    player = Player("Tester")

    # Add regular item
    regular_item = Item("key", "A regular key")
    player.take_item(regular_item)

    # Add AI component
    ai_comp = AIComponent("Tokenizer", "A tokenizer", "tokenizer")
    player.take_item(ai_comp)

    # Check tracking
    assert len(player.inventory) == 2
    assert len(player.ai_components_collected) == 1
    assert ai_comp in player.ai_components_collected
    assert regular_item not in player.ai_components_collected

    print("[PASS]AI component tests passed")


def test_player_parser_level():
    """Test parser level calculation."""
    player = Player("Tester")

    # No components = level 0
    assert player.get_parser_level() == 0

    # Add 3 AI components = level 3
    for i in range(3):
        comp = AIComponent(f"Component {i}", f"Desc {i}", f"type{i}")
        player.take_item(comp)

    assert player.get_parser_level() == 3

    print("[PASS]Parser level tests passed")


def test_player_movement():
    """Test player movement between rooms."""
    room1 = Room("Room 1", "First room")
    room2 = Room("Room 2", "Second room")

    player = Player("Tester", starting_room=room1)

    # Check starting position
    assert player.current_room == room1

    # Move to new room
    player.move_to(room2)
    assert player.current_room == room2

    print("[PASS]Movement tests passed")


def test_player_item_search():
    """Test finding items in inventory."""
    player = Player("Tester")

    item = Item("golden key", "A shiny key", keywords=["key", "golden"])
    player.take_item(item)

    # Test finding by different keywords
    assert player.get_item("key") == item
    assert player.get_item("golden") == item
    assert player.get_item("silver") is None

    print("[PASS]Item search tests passed")


if __name__ == "__main__":
    test_player_inventory()
    test_player_ai_components()
    test_player_parser_level()
    test_player_movement()
    test_player_item_search()
    print("\n[SUCCESS]All player tests passed!")
