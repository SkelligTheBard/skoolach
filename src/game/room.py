"""Room class representing locations in the game world."""

class Room:
    """Represents a location in the game that the player can visit."""

    def __init__(self, name, description, short_desc=None, is_dark=False):
        """
        Initialize a room.

        Args:
            name: The name of the room
            description: Full description shown on first visit or when examined
            short_desc: Brief description for subsequent visits
            is_dark: Whether this room requires a light source to see
        """
        self.name = name
        self.description = description
        self.short_desc = short_desc or name
        self.is_dark = is_dark
        self.exits = {}  # direction -> Room mapping
        self.items = []  # Items in this room
        self.visited = False
        self.locked_exits = {}  # direction -> required_item mapping
        self.enemies = []  # Enemies/obstacles in this room

    def add_exit(self, direction, room, locked=False, required_item=None):
        """
        Add an exit to another room.

        Args:
            direction: Direction name (e.g., 'north', 'south', 'up')
            room: The Room object this exit leads to
            locked: Whether this exit is initially locked
            required_item: Item needed to unlock this exit
        """
        self.exits[direction.lower()] = room
        if locked and required_item:
            self.locked_exits[direction.lower()] = required_item

    def add_item(self, item):
        """Add an item to this room."""
        self.items.append(item)

    def remove_item(self, item):
        """Remove an item from this room."""
        if item in self.items:
            self.items.remove(item)

    def get_item(self, word):
        """Find an item in this room that matches the given word."""
        for item in self.items:
            if item.matches(word):
                return item
        return None

    def get_description(self, has_light=True):
        """
        Get the appropriate description for this room.

        Args:
            has_light: Whether the player has an active light source

        Returns:
            Room description string
        """
        # If room is dark and player has no light, can't see anything
        if self.is_dark and not has_light:
            return (
                "It's pitch black. You can't see anything.\n\n"
                "You need a light source to explore this area."
            )

        # Normal description
        if not self.visited:
            self.visited = True
            desc = self.description
        else:
            desc = self.short_desc

        # Add items if present
        if self.items:
            visible_items = [item.name for item in self.items]
            desc += f"\n\nYou can see: {', '.join(visible_items)}"

        # Add exits
        if self.exits:
            exits_list = list(self.exits.keys())
            desc += f"\n\nExits: {', '.join(exits_list)}"

        return desc

    def can_go(self, direction, player_inventory):
        """
        Check if the player can go in a direction.

        Args:
            direction: The direction to check
            player_inventory: List of items the player has

        Returns:
            Tuple of (can_go: bool, message: str)
        """
        direction = direction.lower()

        if direction not in self.exits:
            return False, "You can't go that way."

        if direction in self.locked_exits:
            required = self.locked_exits[direction]
            if not any(item.name == required for item in player_inventory):
                return False, f"The way is blocked. You need the {required}."
            # Unlock the exit permanently once accessed with the right item
            del self.locked_exits[direction]

        return True, "OK"

    def get_exit(self, direction):
        """Get the room in a given direction."""
        return self.exits.get(direction.lower())
