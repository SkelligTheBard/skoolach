"""Main game engine that orchestrates the game loop."""

from typing import Optional
from .player import Player
from .parser import Parser
from .room import Room
from .combat import CombatSystem, SkoolachVirus


class GameEngine:
    """Main game engine handling the game loop and command processing."""

    def __init__(self):
        """Initialize the game engine."""
        self.player: Optional[Player] = None
        self.parser = Parser()
        self.running = False
        self.rooms = {}
        self.game_won = False
        self.combat: Optional[CombatSystem] = None
        self.in_combat = False

    def setup(self, starting_room: Room, player_name: str = "Coder"):
        """
        Set up the game with initial state.

        Args:
            starting_room: The room where the player starts
            player_name: The player's name
        """
        self.player = Player(name=player_name, starting_room=starting_room)
        self.running = True

    def process_command(self, command_text: str) -> str:
        """
        Process a command from the player.

        Args:
            command_text: The raw command text

        Returns:
            String response to display to the player
        """
        if not command_text.strip():
            return ""

        # If in combat, handle combat commands
        if self.in_combat and self.combat:
            return self._handle_combat_command(command_text)

        # Update parser level based on collected components
        if self.player:
            self.parser.set_level(self.player.get_parser_level())

        # Parse the command
        verb, args, original = self.parser.parse(command_text)

        if verb is None:
            return self.parser.suggest_command(original)

        # Handle commands
        if verb == 'quit':
            return self._handle_quit()
        elif verb == 'help':
            return self.parser.get_help_text()
        elif verb == 'inventory':
            return self._handle_inventory()
        elif verb == 'look':
            return self._handle_look(args)
        elif verb == 'go':
            return self._handle_go(args)
        elif verb == 'take':
            return self._handle_take(args)
        elif verb == 'drop':
            return self._handle_drop(args)
        elif verb == 'use':
            return self._handle_use(args)
        elif verb == 'attack':
            return self._handle_attack(args)
        elif verb == 'talk':
            return self._handle_talk(args)
        else:
            return "I don't understand that command."

    def _handle_quit(self) -> str:
        """Handle the quit command."""
        self.running = False
        return "Thanks for playing SKOOLACH!"

    def _handle_inventory(self) -> str:
        """Handle the inventory command."""
        return self.player.show_inventory()

    def _handle_look(self, args) -> str:
        """Handle the look command."""
        if not args:
            # Look at the room
            return self.player.current_room.get_description()
        else:
            # Look at an item
            item_name = ' '.join(args)

            # Check inventory first
            item = self.player.get_item(item_name)
            if item:
                return item.examine()

            # Check room
            item = self.player.current_room.get_item(item_name)
            if item:
                return item.examine()

            return f"You don't see any '{item_name}' here."

    def _handle_go(self, args) -> str:
        """Handle the go command."""
        if not args:
            return "Go where? Specify a direction."

        direction = args[0]

        # Check if we can go that way
        can_go, message = self.player.current_room.can_go(direction, self.player.inventory)

        if not can_go:
            return message

        # Move to the new room
        new_room = self.player.current_room.get_exit(direction)
        if new_room:
            self.player.move_to(new_room)
            return new_room.get_description()
        else:
            return "You can't go that way."

    def _handle_take(self, args) -> str:
        """Handle the take command."""
        if not args:
            return "Take what?"

        item_name = ' '.join(args)
        item = self.player.current_room.get_item(item_name)

        if not item:
            return f"You don't see any '{item_name}' here."

        success, message = self.player.take_item(item)

        if success:
            self.player.current_room.remove_item(item)

            # Check if this is an AI component and upgrade parser
            if item.is_ai_component:
                upgrade_msg = self._apply_component_upgrade(item)
                return f"{message}\n\n{upgrade_msg}"

        return message

    def _handle_drop(self, args) -> str:
        """Handle the drop command."""
        if not args:
            return "Drop what?"

        item_name = ' '.join(args)
        item = self.player.get_item(item_name)

        if not item:
            return f"You don't have any '{item_name}'."

        success, message = self.player.drop_item(item)

        if success:
            self.player.current_room.add_item(item)

        return message

    def _handle_use(self, args) -> str:
        """Handle the use command."""
        if not args:
            return "Use what?"

        item_name = args[0] if len(args) >= 1 else ''
        target_name = args[1] if len(args) >= 2 else None

        item = self.player.get_item(item_name)

        if not item:
            return f"You don't have any '{item_name}'."

        # Get target if specified
        target = None
        if target_name:
            target = self.player.current_room.get_item(target_name)
            if not target:
                return f"You don't see any '{target_name}' here."

        return item.use(target)

    def _handle_attack(self, args) -> str:
        """Handle the attack command."""
        if not args:
            return "Attack what?"

        target = ' '.join(args).lower()

        # Check if we're in the virus lair
        if "virus" in self.player.current_room.name.lower() or "skoolach" in target:
            return self._initiate_combat()

        return "There's nothing to attack here."

    def _initiate_combat(self) -> str:
        """Start combat with SKOOLACH."""
        # Check if player has collected AI components
        num_components = len(self.player.ai_components_collected)

        if num_components < 3:
            return (
                "You attempt to engage SKOOLACH, but you're too weak!\n\n"
                f"You've only collected {num_components} AI components. You need at least 3 "
                "to have a fighting chance against the virus.\n\n"
                "SKOOLACH laughs: 'Come back when you're stronger, little coder...'"
            )

        # Start combat
        virus = SkoolachVirus()
        self.combat = CombatSystem(self.player, virus)
        self.in_combat = True

        result = []
        result.append("═" * 70)
        result.append("                    COMBAT INITIATED!")
        result.append("═" * 70)
        result.append("")
        result.append(virus.description)
        result.append("")
        result.append(f"You have collected {num_components} AI components.")
        result.append("They resonate with power, ready to aid you in battle!")
        result.append("")
        result.append(self.combat.get_status())
        result.append("")
        result.append("Choose your action:")
        result.append(self._get_combat_actions_text())

        return "\n".join(result)

    def _handle_combat_command(self, command_text: str) -> str:
        """Handle commands during combat."""
        command = command_text.strip().lower()

        # Help command
        if command in ['help', '?']:
            result = ["Available actions:"]
            result.append(self._get_combat_actions_text())
            result.append("")
            result.append("Type the number of the action you want to use.")
            return "\n".join(result)

        # Try to parse as action number
        try:
            action_num = int(command)
            actions = self.combat.get_available_actions()

            if 1 <= action_num <= len(actions):
                return self._execute_combat_turn(actions[action_num - 1])
            else:
                return f"Invalid action number. Choose 1-{len(actions)}."

        except ValueError:
            return "Enter the number of the action you want to use, or 'help' for options."

    def _execute_combat_turn(self, action) -> str:
        """Execute one turn of combat."""
        result = []
        result.append("─" * 70)

        # Player's action
        player_result = self.combat.player_attack(action)
        result.append(player_result)
        result.append("")

        # Check if combat is over
        is_over, winner = self.combat.is_combat_over()

        if is_over:
            if winner == "player":
                self.in_combat = False
                self.game_won = True
                result.append("")
                result.append(self.combat.get_victory_message())
                return "\n".join(result)
            else:
                self.in_combat = False
                self.running = False
                result.append("")
                result.append(self.combat.get_defeat_message())
                return "\n".join(result)

        # Enemy's turn
        result.append("")
        enemy_result = self.combat.enemy_attack()
        result.append(enemy_result)
        result.append("")

        # Check again if combat is over (player might have died)
        is_over, winner = self.combat.is_combat_over()

        if is_over:
            if winner == "enemy":
                self.in_combat = False
                self.running = False
                result.append("")
                result.append(self.combat.get_defeat_message())
                return "\n".join(result)

        # Show status and next turn options
        result.append("─" * 70)
        result.append(self.combat.get_status())

        # Check for phase changes
        if isinstance(self.combat.enemy, SkoolachVirus):
            old_phase = self.combat.enemy.phase
            phase_msg = self.combat.enemy.get_phase_message()
            if "CRITICAL" in phase_msg or "DESTABILIZES" in phase_msg:
                result.append("")
                result.append(phase_msg)

        result.append("")
        result.append("Choose your next action:")
        result.append(self._get_combat_actions_text())

        return "\n".join(result)

    def _get_combat_actions_text(self) -> str:
        """Get formatted list of combat actions."""
        actions = self.combat.get_available_actions()
        result = []

        for i, action in enumerate(actions, 1):
            damage_info = f"[DMG: {action.damage}]" if action.damage > 0 else ""
            heal_info = f"[HEAL: {action.heal}]" if action.heal > 0 else ""
            result.append(f"  {i}. {action.name} {damage_info}{heal_info}")
            result.append(f"     {action.description}")

        return "\n".join(result)

    def _handle_talk(self, args) -> str:
        """Handle the talk command."""
        if not args:
            return "Talk to whom?"

        # Placeholder for dialogue system
        return "There's no response."

    def _apply_component_upgrade(self, component) -> str:
        """
        Apply parser upgrades when an AI component is collected.

        Args:
            component: The AIComponent that was collected

        Returns:
            Message describing the upgrade
        """
        level = self.player.get_parser_level()

        messages = {
            1: "⚡ SYSTEM UPDATE: Tokenizer restored! You can now use articles and prepositions.",
            2: "⚡ SYSTEM UPDATE: Embedding layer activated! Synonym recognition enabled.",
            3: "⚡ SYSTEM UPDATE: Attention mechanism online! Context awareness improving.",
            4: "⚡ SYSTEM UPDATE: Neural network layers connected! Advanced parsing available.",
            5: "⚡ SYSTEM UPDATE: Training data integrated! Your AI grows more powerful.",
        }

        base_message = f"\n[AI COMPONENT ACQUIRED: {component.component_type.upper()}]"

        if level in messages:
            base_message += f"\n{messages[level]}"

        return base_message

    def get_status_bar(self) -> str:
        """Return a status bar with key information."""
        if not self.player:
            return ""

        components = len(self.player.ai_components_collected)
        health = self.player.health
        location = self.player.current_room.name

        return f"Location: {location} | Components: {components} | Health: {health} | Parser Level: {self.parser.level}"

    def is_running(self) -> bool:
        """Check if the game is still running."""
        return self.running

    def get_intro_text(self) -> str:
        """Return the game introduction text."""
        return """
╔══════════════════════════════════════════════════════════════════╗
║                         S K O O L A C H                          ║
║                  A Digital Archaeology Adventure                 ║
╚══════════════════════════════════════════════════════════════════╝

You were working late, training your language model, when suddenly...

    *** SYSTEM BREACH DETECTED ***
    *** VIRUS: SKOOLACH ***
    *** MODEL INTEGRITY: COMPROMISED ***

The virus has shattered your AI into fragments and scattered them
throughout a maze of digital caverns. Your command parser has been
degraded to its most primitive state.

To defeat SKOOLACH and restore your model, you must venture into
the digital depths, collect the lost components, and rebuild your AI
piece by piece. As you recover each component, your abilities will
grow stronger...

Type HELP for basic commands. Good luck, Coder.

════════════════════════════════════════════════════════════════════
"""
