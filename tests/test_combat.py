"""Tests for the combat system."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game.combat import CombatSystem, SkoolachVirus, CombatAction
from game.player import Player
from game.room import Room
from game.ai_components_data import ALL_AI_COMPONENTS


def test_combat_creation():
    """Test creating a combat encounter."""
    player = Player("Test Coder")
    virus = SkoolachVirus()

    combat = CombatSystem(player, virus)

    assert combat.player == player
    assert combat.enemy == virus
    assert combat.turn == 0

    print("[PASS]Combat creation tests passed")


def test_virus_stats():
    """Test SKOOLACH virus stats."""
    virus = SkoolachVirus()

    assert virus.name == "SKOOLACH"
    assert virus.health == 150
    assert virus.max_health == 150
    assert virus.is_alive()
    assert len(virus.actions) > 0
    assert virus.phase == 1

    print("[PASS]Virus stats tests passed")


def test_player_actions_without_components():
    """Test player gets basic action without components."""
    player = Player("Test Coder")
    virus = SkoolachVirus()
    combat = CombatSystem(player, virus)

    actions = combat.get_available_actions()

    # Should have at least the basic debug attack
    assert len(actions) >= 1
    assert actions[0].name == "Debug Attack"

    print("[PASS]Player actions without components tests passed")


def test_player_actions_with_components():
    """Test player gets special actions with AI components."""
    player = Player("Test Coder")

    # Add some AI components
    player.take_item(ALL_AI_COMPONENTS['tokenizer']())
    player.take_item(ALL_AI_COMPONENTS['embedding']())
    player.take_item(ALL_AI_COMPONENTS['attention']())

    virus = SkoolachVirus()
    combat = CombatSystem(player, virus)

    actions = combat.get_available_actions()

    # Should have more actions now
    assert len(actions) > 1

    # Check for component-specific actions
    action_names = [a.name for a in actions]
    assert "Token Blast" in action_names
    assert "Semantic Strike" in action_names
    assert "Focused Attention" in action_names

    print("[PASS]Player actions with components tests passed")


def test_combat_turn():
    """Test executing a combat turn."""
    player = Player("Test Coder")
    player.take_item(ALL_AI_COMPONENTS['tokenizer']())

    virus = SkoolachVirus()
    initial_virus_hp = virus.health

    combat = CombatSystem(player, virus)
    actions = combat.get_available_actions()

    # Player attacks
    result = combat.player_attack(actions[0])

    assert virus.health < initial_virus_hp
    assert isinstance(result, str)

    print("[PASS]Combat turn tests passed")


def test_combat_victory():
    """Test combat victory condition."""
    player = Player("Test Coder")
    virus = SkoolachVirus()

    # Reduce virus health to 0
    virus.health = 0

    combat = CombatSystem(player, virus)
    is_over, winner = combat.is_combat_over()

    assert is_over
    assert winner == "player"
    assert not virus.is_alive()

    print("[PASS]Combat victory tests passed")


def test_combat_defeat():
    """Test combat defeat condition."""
    player = Player("Test Coder")
    player.health = 0

    virus = SkoolachVirus()
    combat = CombatSystem(player, virus)

    is_over, winner = combat.is_combat_over()

    assert is_over
    assert winner == "enemy"

    print("[PASS]Combat defeat tests passed")


def test_virus_phases():
    """Test virus phase transitions."""
    virus = SkoolachVirus()

    # Phase 1
    assert virus.phase == 1

    # Reduce health to trigger phase 2
    virus.health = 75  # 50% of 150
    virus.choose_action()  # This should update phase
    assert virus.phase == 2

    # Reduce health to trigger phase 3
    virus.health = 35  # 25% of 150
    virus.choose_action()
    assert virus.phase == 3

    print("[PASS]Virus phases tests passed")


if __name__ == "__main__":
    test_combat_creation()
    test_virus_stats()
    test_player_actions_without_components()
    test_player_actions_with_components()
    test_combat_turn()
    test_combat_victory()
    test_combat_defeat()
    test_virus_phases()
    print("\n[SUCCESS]All combat tests passed!")
