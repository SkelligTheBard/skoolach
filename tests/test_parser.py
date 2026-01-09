"""Tests for the text parser."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game.parser import Parser


def test_parser_level_0_basic_commands():
    """Test basic level 0 parsing."""
    parser = Parser()
    parser.set_level(0)

    # Test simple go command
    verb, args, _ = parser.parse("go north")
    assert verb == "go"
    assert args == ["north"]

    # Test take command
    verb, args, _ = parser.parse("take key")
    assert verb == "take"
    assert args == ["key"]

    # Test inventory
    verb, args, _ = parser.parse("inventory")
    assert verb == "inventory"
    assert args == []

    # Test direction shortcut
    verb, args, _ = parser.parse("n")
    assert verb == "go"
    assert args == ["north"]

    print("[PASS] Level 0 parsing tests passed")


def test_parser_level_1_articles():
    """Test level 1 parsing with articles."""
    parser = Parser()
    parser.set_level(1)

    # Test with articles
    verb, args, _ = parser.parse("take the key")
    assert verb == "take"
    assert "key" in args
    assert "the" not in args

    # Test with prepositions
    verb, args, _ = parser.parse("go to the north")
    assert verb == "go"
    assert "north" in args

    print("[PASS]Level 1 parsing tests passed")


def test_parser_synonyms():
    """Test verb synonyms."""
    parser = Parser()
    parser.set_level(0)

    # Test take synonyms
    for synonym in ["get", "grab", "pick"]:
        verb, _, _ = parser.parse(f"{synonym} key")
        assert verb == "take", f"Failed for synonym: {synonym}"

    # Test look synonyms
    for synonym in ["examine", "inspect", "check"]:
        verb, _, _ = parser.parse(f"{synonym} door")
        assert verb == "look", f"Failed for synonym: {synonym}"

    print("[PASS]Synonym tests passed")


def test_parser_invalid_commands():
    """Test invalid command handling."""
    parser = Parser()
    parser.set_level(0)

    # Test unknown verb
    verb, args, _ = parser.parse("dance around")
    assert verb is None

    # Test empty input
    verb, args, _ = parser.parse("")
    assert verb is None

    print("[PASS]Invalid command tests passed")


if __name__ == "__main__":
    test_parser_level_0_basic_commands()
    test_parser_level_1_articles()
    test_parser_synonyms()
    test_parser_invalid_commands()
    print("\n[SUCCESS] All parser tests passed!")
