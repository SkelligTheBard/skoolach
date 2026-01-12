"""Combat system for battling the SKOOLACH virus."""

import random
from typing import List, Optional, Tuple
from .item import AIComponent


class CombatAction:
    """Represents an action that can be taken in combat."""

    def __init__(self, name: str, description: str, damage: int = 0,
                 heal: int = 0, required_component: Optional[str] = None):
        """
        Initialize a combat action.

        Args:
            name: Action name
            description: What the action does
            damage: Damage dealt to enemy
            heal: Health restored to player
            required_component: AI component type required to use this action
        """
        self.name = name
        self.description = description
        self.damage = damage
        self.heal = heal
        self.required_component = required_component


class Enemy:
    """Base enemy class."""

    def __init__(self, name: str, description: str, max_health: int):
        """
        Initialize an enemy.

        Args:
            name: Enemy name
            description: Enemy description
            max_health: Maximum health points
        """
        self.name = name
        self.description = description
        self.max_health = max_health
        self.health = max_health
        self.actions: List[CombatAction] = []

    def is_alive(self) -> bool:
        """Check if enemy is still alive."""
        return self.health > 0

    def take_damage(self, amount: int) -> str:
        """
        Apply damage to enemy.

        Args:
            amount: Damage amount

        Returns:
            Description of the result
        """
        self.health = max(0, self.health - amount)
        if self.health == 0:
            return f"{self.name} has been defeated!"
        return f"{self.name} takes {amount} damage! ({self.health}/{self.max_health} HP remaining)"

    def choose_action(self) -> CombatAction:
        """
        Choose an action to perform (AI).

        Returns:
            The chosen CombatAction
        """
        if not self.actions:
            return CombatAction("struggle", "The enemy struggles weakly.", damage=5)
        return random.choice(self.actions)


class SkoolachVirus(Enemy):
    """The final boss - SKOOLACH virus."""

    def __init__(self):
        """Initialize the SKOOLACH virus boss."""
        super().__init__(
            name="SKOOLACH",
            description="A massive virus of corrupted code, pulsing with malicious energy.",
            max_health=150
        )

        # Define virus attacks
        self.actions = [
            CombatAction(
                name="Memory Corruption",
                description="SKOOLACH corrupts your memory, dealing moderate damage.",
                damage=15
            ),
            CombatAction(
                name="Parser Degradation",
                description="SKOOLACH attacks your language processing, dealing heavy damage.",
                damage=25
            ),
            CombatAction(
                name="Data Leak",
                description="SKOOLACH siphons your training data, dealing light damage.",
                damage=10
            ),
            CombatAction(
                name="Stack Overflow",
                description="SKOOLACH causes a cascade failure, dealing massive damage!",
                damage=30
            ),
            CombatAction(
                name="Regenerate",
                description="SKOOLACH absorbs corrupted data to heal itself.",
                damage=0,
                heal=20
            ),
        ]

        # Boss phases
        self.phase = 1

    def choose_action(self) -> CombatAction:
        """Choose an action based on current health/phase."""
        health_percent = self.health / self.max_health

        # Phase transitions
        if health_percent <= 0.5 and self.phase == 1:
            self.phase = 2
        elif health_percent <= 0.25 and self.phase == 2:
            self.phase = 3

        # Phase 3: Desperate, uses more powerful attacks
        if self.phase == 3:
            return random.choice([a for a in self.actions if a.damage >= 20])

        # Phase 2: Mix of attacks
        elif self.phase == 2:
            # Sometimes heal
            if health_percent < 0.4 and random.random() < 0.3:
                return [a for a in self.actions if a.name == "Regenerate"][0]
            return random.choice(self.actions)

        # Phase 1: Normal attacks
        else:
            return random.choice([a for a in self.actions if a.damage > 0 and a.damage < 30])

    def get_phase_message(self) -> str:
        """Get message for current phase."""
        if self.phase == 1:
            return "SKOOLACH writhes menacingly..."
        elif self.phase == 2:
            return "*** SKOOLACH'S CODE DESTABILIZES! The virus grows more aggressive! ***"
        else:
            return "*** CRITICAL: SKOOLACH ENTERS FINAL FORM! MAXIMUM CORRUPTION! ***"


class CombatSystem:
    """Manages combat encounters."""

    def __init__(self, player, enemy: Enemy):
        """
        Initialize combat.

        Args:
            player: The Player object
            enemy: The Enemy to fight
        """
        self.player = player
        self.enemy = enemy
        self.turn = 0
        self.combat_log: List[str] = []
        self.player_actions: List[CombatAction] = []

        # Generate available actions based on collected AI components
        self._generate_player_actions()

    def _generate_player_actions(self):
        """Generate actions available to player based on AI components."""
        # Basic action always available
        self.player_actions.append(
            CombatAction(
                name="Debug Attack",
                description="A basic debugging attempt. Weak but reliable.",
                damage=10
            )
        )

        # Actions based on collected AI components
        component_actions = {
            'tokenizer': CombatAction(
                name="Token Blast",
                description="Break down the virus into manageable tokens and eliminate them.",
                damage=20,
                required_component='tokenizer'
            ),
            'embedding': CombatAction(
                name="Semantic Strike",
                description="Use vector space to find the virus's weak points.",
                damage=25,
                required_component='embedding'
            ),
            'attention': CombatAction(
                name="Focused Attention",
                description="Focus all processing power on the virus's critical components.",
                damage=30,
                required_component='attention'
            ),
            'neural_layer': CombatAction(
                name="Neural Surge",
                description="Channel neural network power through all layers.",
                damage=35,
                required_component='neural_layer'
            ),
            'training_data': CombatAction(
                name="Knowledge Beam",
                description="Deploy accumulated knowledge against the virus.",
                damage=28,
                required_component='training_data'
            ),
            'optimizer': CombatAction(
                name="Gradient Descent",
                description="Optimize damage output through iterative improvement.",
                damage=32,
                required_component='optimizer'
            ),
            'inference': CombatAction(
                name="Prediction Strike",
                description="Predict and counter the virus's next move.",
                damage=40,
                required_component='inference'
            ),
            'context': CombatAction(
                name="Contextual Barrage",
                description="Use long-term context to overwhelm the virus.",
                damage=38,
                required_component='context'
            ),
        }

        # Add actions for components the player has collected
        for component in self.player.ai_components_collected:
            comp_type = component.component_type
            if comp_type in component_actions:
                self.player_actions.append(component_actions[comp_type])

        # Special healing action if player has optimizer
        if any(c.component_type == 'optimizer' for c in self.player.ai_components_collected):
            self.player_actions.append(
                CombatAction(
                    name="Self-Optimize",
                    description="Optimize your own systems to restore health.",
                    heal=30,
                    required_component='optimizer'
                )
            )

    def get_available_actions(self) -> List[CombatAction]:
        """Get list of actions player can currently perform."""
        return self.player_actions

    def player_attack(self, action: CombatAction) -> str:
        """
        Player performs an attack action.

        Args:
            action: The CombatAction to perform

        Returns:
            Result description
        """
        result = []
        result.append(f"You use {action.name}!")
        result.append(action.description)

        if action.damage > 0:
            # Add some randomness (90-110% damage)
            actual_damage = int(action.damage * random.uniform(0.9, 1.1))
            damage_msg = self.enemy.take_damage(actual_damage)
            result.append(damage_msg)

        if action.heal > 0:
            old_health = self.player.health
            self.player.health = min(100, self.player.health + action.heal)
            healed = self.player.health - old_health
            result.append(f"You restore {healed} health! ({self.player.health}/100 HP)")

        return "\n".join(result)

    def enemy_attack(self) -> str:
        """
        Enemy performs an attack.

        Returns:
            Result description
        """
        action = self.enemy.choose_action()
        result = []

        result.append(f"{self.enemy.name} uses {action.name}!")
        result.append(action.description)

        if action.damage > 0:
            # Apply damage to player
            actual_damage = int(action.damage * random.uniform(0.9, 1.1))
            self.player.health = max(0, self.player.health - actual_damage)
            result.append(f"You take {actual_damage} damage! ({self.player.health}/100 HP)")

        if action.heal > 0:
            old_health = self.enemy.health
            self.enemy.health = min(self.enemy.max_health, self.enemy.health + action.heal)
            healed = self.enemy.health - old_health
            result.append(f"{self.enemy.name} restores {healed} health! ({self.enemy.health}/{self.enemy.max_health} HP)")

        return "\n".join(result)

    def is_combat_over(self) -> Tuple[bool, Optional[str]]:
        """
        Check if combat is over.

        Returns:
            Tuple of (is_over, winner)
        """
        if not self.enemy.is_alive():
            return True, "player"
        if self.player.health <= 0:
            return True, "enemy"
        return False, None

    def get_status(self) -> str:
        """Get combat status display."""
        return f"YOUR HP: {self.player.health}/100 | {self.enemy.name} HP: {self.enemy.health}/{self.enemy.max_health}"

    def get_victory_message(self) -> str:
        """Get victory message."""
        return """
╔══════════════════════════════════════════════════════════════════╗
║                        VICTORY!                                  ║
╚══════════════════════════════════════════════════════════════════╝

SKOOLACH disintegrates into fragments of corrupted code, which
dissolve into nothingness. The digital cave shudders and begins
to stabilize.

Your AI model's components resonate with each other, clicking into
place. The parser, the embeddings, the attention mechanisms, the
neural layers - everything you've collected begins to reconstruct
itself.

A message appears:

    *** SYSTEM RESTORED ***
    *** AI MODEL: OPERATIONAL ***
    *** ALL COMPONENTS: INTEGRATED ***

You've done it. Your AI is whole again, stronger than before.
The virus is defeated.

But more importantly... you now understand how it all works.
From tokens to transformers, from data to deployment.

The journey through the digital depths has taught you the
architecture of intelligence itself.

╔══════════════════════════════════════════════════════════════════╗
║              CONGRATULATIONS - YOU COMPLETED SKOOLACH!           ║
╚══════════════════════════════════════════════════════════════════╝
"""

    def get_defeat_message(self) -> str:
        """Get defeat message."""
        return """
╔══════════════════════════════════════════════════════════════════╗
║                        SYSTEM FAILURE                            ║
╚══════════════════════════════════════════════════════════════════╝

SKOOLACH's corruption overwhelms you. Your consciousness fragments
and scatters throughout the digital void...

    *** CRITICAL ERROR ***
    *** SYSTEM COMPROMISED ***
    *** MODEL UNRECOVERABLE ***

Without all the AI components, you weren't strong enough to defeat
the virus. The model remains broken, lost in the depths of
corrupted data.

Perhaps in another timeline, with more components collected,
the outcome would be different...

GAME OVER
"""
