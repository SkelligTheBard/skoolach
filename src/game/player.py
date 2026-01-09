"""Player class representing the player character."""

class Player:
    """Represents the player character and their state."""

    def __init__(self, name="Coder", starting_room=None):
        """
        Initialize the player.

        Args:
            name: The player's name
            starting_room: The room where the player starts
        """
        self.name = name
        self.current_room = starting_room
        self.inventory = []
        self.ai_components_collected = []  # Track AI components separately
        self.max_inventory = 10
        self.health = 100  # For combat with the virus

    def take_item(self, item):
        """
        Add an item to inventory.

        Args:
            item: The Item to add

        Returns:
            Tuple of (success: bool, message: str)
        """
        if len(self.inventory) >= self.max_inventory:
            return False, "Your inventory is full."

        if not item.takeable:
            return False, f"You can't take the {item.name}."

        self.inventory.append(item)

        # Track AI components
        if item.is_ai_component:
            self.ai_components_collected.append(item)

        return True, f"You take the {item.name}."

    def drop_item(self, item):
        """
        Remove an item from inventory.

        Args:
            item: The Item to remove

        Returns:
            Tuple of (success: bool, message: str)
        """
        if item not in self.inventory:
            return False, f"You don't have the {item.name}."

        self.inventory.remove(item)

        # Update AI components tracking
        if item.is_ai_component and item in self.ai_components_collected:
            self.ai_components_collected.remove(item)

        return True, f"You drop the {item.name}."

    def get_item(self, word):
        """Find an item in inventory that matches the given word."""
        for item in self.inventory:
            if item.matches(word):
                return item
        return None

    def has_item(self, item_name):
        """Check if player has an item by name."""
        return any(item.name.lower() == item_name.lower() for item in self.inventory)

    def show_inventory(self):
        """Return a string representation of the inventory."""
        if not self.inventory:
            return "You are carrying nothing."

        items = [item.name for item in self.inventory]
        result = f"You are carrying:\n  " + "\n  ".join(items)

        # Show AI component count
        if self.ai_components_collected:
            result += f"\n\nAI Components collected: {len(self.ai_components_collected)}"

        return result

    def move_to(self, room):
        """Move the player to a new room."""
        self.current_room = room

    def get_parser_level(self):
        """
        Calculate parser sophistication based on collected AI components.

        Returns:
            Integer level (0 = basic, higher = more sophisticated)
        """
        return len(self.ai_components_collected)
