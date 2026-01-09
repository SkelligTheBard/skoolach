"""Text parser that evolves as the player collects AI components."""

import re
from typing import Tuple, List, Optional


class Parser:
    """
    Text parser that starts simple and becomes more sophisticated.

    The parser has multiple levels:
    Level 0: Basic two-word commands (VERB NOUN)
    Level 1: Three-word commands with prepositions (VERB NOUN PREP NOUN)
    Level 2: Synonyms and basic context understanding
    Level 3: Natural language with article handling
    Level 4+: Advanced parsing with intent recognition
    """

    def __init__(self):
        """Initialize the parser with basic capabilities."""
        self.level = 0

        # Basic verb mappings (available at all levels)
        self.verbs = {
            'go': ['go', 'move', 'walk', 'run', 'travel', 'head'],
            'take': ['take', 'get', 'grab', 'pick', 'acquire'],
            'drop': ['drop', 'leave', 'discard', 'put'],
            'look': ['look', 'examine', 'inspect', 'check', 'view', 'describe'],
            'inventory': ['inventory', 'inv', 'i', 'items'],
            'use': ['use', 'activate', 'apply'],
            'help': ['help', '?', 'commands'],
            'quit': ['quit', 'exit', 'q'],
            'attack': ['attack', 'fight', 'hit', 'strike', 'kill'],
            'talk': ['talk', 'speak', 'chat', 'say'],
        }

        # Direction shortcuts
        self.directions = {
            'n': 'north',
            's': 'south',
            'e': 'east',
            'w': 'west',
            'ne': 'northeast',
            'nw': 'northwest',
            'se': 'southeast',
            'sw': 'southwest',
            'u': 'up',
            'd': 'down',
        }

        # Articles and prepositions to strip (at higher levels)
        self.articles = ['a', 'an', 'the']
        self.prepositions = ['at', 'to', 'with', 'on', 'in', 'from']

    def set_level(self, level: int):
        """Set the parser sophistication level."""
        self.level = level

    def parse(self, input_text: str) -> Tuple[Optional[str], List[str], str]:
        """
        Parse input text into a command.

        Args:
            input_text: The raw input from the player

        Returns:
            Tuple of (verb, arguments, original_text)
            Returns (None, [], input_text) if parsing fails
        """
        if not input_text or not input_text.strip():
            return None, [], input_text

        original = input_text.strip()
        text = original.lower().strip()

        # Level 0: Very basic parsing (just verb, or verb + noun)
        if self.level == 0:
            return self._parse_level_0(text, original)

        # Level 1+: Handle articles and multiple words
        if self.level >= 1:
            return self._parse_level_1(text, original)

        return None, [], original

    def _parse_level_0(self, text: str, original: str) -> Tuple[Optional[str], List[str], str]:
        """
        Level 0 parsing: Only understand VERB or VERB NOUN.

        Examples:
            "go north" -> ('go', ['north'])
            "take key" -> ('take', ['key'])
            "inventory" -> ('inventory', [])
            "north" -> ('go', ['north']) # shortcut
        """
        words = text.split()

        if not words:
            return None, [], original

        # Check if first word is a direction shortcut
        if len(words) == 1 and words[0] in self.directions:
            return 'go', [self.directions[words[0]]], original

        # Check for full direction as standalone command
        if len(words) == 1 and words[0] in ['north', 'south', 'east', 'west', 'up', 'down',
                                              'northeast', 'northwest', 'southeast', 'southwest']:
            return 'go', [words[0]], original

        # Find the verb
        verb = self._find_verb(words[0])

        if not verb:
            return None, [], original

        # Commands that take no arguments
        if verb in ['inventory', 'help', 'quit', 'look'] and len(words) == 1:
            return verb, [], original

        # Two-word commands
        if len(words) == 2:
            return verb, [words[1]], original

        # At level 0, we don't understand more than 2 words
        if len(words) > 2:
            return None, [], original

        return verb, [], original

    def _parse_level_1(self, text: str, original: str) -> Tuple[Optional[str], List[str], str]:
        """
        Level 1+ parsing: Handle articles, prepositions, and multi-word nouns.

        Examples:
            "take the key" -> ('take', ['key'])
            "go to the north" -> ('go', ['north'])
            "use key on door" -> ('use', ['key', 'door'])
        """
        words = text.split()

        if not words:
            return None, [], original

        # Check for direction shortcuts
        if len(words) == 1 and words[0] in self.directions:
            return 'go', [self.directions[words[0]]], original

        # Find the verb
        verb = self._find_verb(words[0])

        if not verb:
            # At higher levels, try to infer verb
            if self.level >= 2:
                # If it's a direction, assume 'go'
                if words[0] in ['north', 'south', 'east', 'west', 'up', 'down',
                                'northeast', 'northwest', 'southeast', 'southwest']:
                    return 'go', [words[0]], original
            return None, [], original

        # Remove verb from words
        words = words[1:]

        # Commands that take no arguments
        if verb in ['inventory', 'help', 'quit'] and not words:
            return verb, [], original

        # 'look' with no args means look at room
        if verb == 'look' and not words:
            return verb, [], original

        # Remove articles and prepositions at level 1+
        if self.level >= 1:
            words = [w for w in words if w not in self.articles and w not in self.prepositions]

        return verb, words, original

    def _find_verb(self, word: str) -> Optional[str]:
        """Find the canonical verb for a given word."""
        for canonical, synonyms in self.verbs.items():
            if word in synonyms:
                return canonical
        return None

    def get_help_text(self) -> str:
        """Return help text appropriate for the current parser level."""
        if self.level == 0:
            return """
BASIC COMMANDS (VIRUS-DEGRADED MODE):
  GO <direction>     - Move in a direction (north, south, east, west, up, down)
  TAKE <item>        - Pick up an item
  DROP <item>        - Drop an item
  LOOK               - Look around the current room
  LOOK <item>        - Examine an item
  INVENTORY (or I)   - Check your inventory
  USE <item>         - Use an item
  HELP               - Show this help
  QUIT               - Exit the game

Note: The virus has severely limited your command parser.
      Collect AI components to restore natural language understanding!
"""
        elif self.level == 1:
            return """
IMPROVED COMMANDS (TOKENIZER RESTORED):
  You can now use articles: "take THE key", "go TO the north"
  Multiple word objects are better understood.
  Direction shortcuts work: n, s, e, w, u, d

All basic commands still work, but the parser is becoming more flexible!
"""
        else:
            return """
ADVANCED COMMANDS (AI-ENHANCED MODE):
  The parser now understands natural language!
  Try things like: "examine the strange device carefully"
                  "use the key on the door"
                  "attack virus with debugger"

Synonyms work: take/grab/get, look/examine/inspect, go/move/walk

Your AI is growing more powerful...
"""

    def suggest_command(self, failed_input: str) -> str:
        """Suggest a valid command based on failed input."""
        if self.level == 0:
            return "Try using simple two-word commands like 'GO NORTH' or 'TAKE ITEM'."
        else:
            return "I don't understand that command. Type HELP for available commands."
