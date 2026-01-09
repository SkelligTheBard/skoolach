"""Item class representing objects in the game world."""

class Item:
    """Represents an item that can be picked up, examined, or used."""

    def __init__(self, name, description, takeable=True, keywords=None):
        """
        Initialize an item.

        Args:
            name: The display name of the item
            description: Full description when examined
            takeable: Whether the item can be picked up
            keywords: List of words that can refer to this item
        """
        self.name = name
        self.description = description
        self.takeable = takeable
        self.keywords = keywords or [name.lower()]
        self.is_ai_component = False  # Will be True for AI parts

    def examine(self):
        """Return the description of the item."""
        return self.description

    def use(self, target=None):
        """
        Use the item. Override in subclasses for specific behavior.

        Args:
            target: Optional target for the item's use

        Returns:
            String describing the result of using the item
        """
        return f"You can't use the {self.name} that way."

    def matches(self, word):
        """Check if a word matches this item."""
        return word.lower() in self.keywords


class AIComponent(Item):
    """Special item representing a component of the AI model."""

    def __init__(self, name, description, component_type, parser_upgrade=None):
        """
        Initialize an AI component.

        Args:
            name: The display name of the component
            description: Full description
            component_type: Type of AI component (e.g., 'tokenizer', 'embedding')
            parser_upgrade: Function to upgrade parser when collected
        """
        super().__init__(name, description, takeable=True)
        self.is_ai_component = True
        self.component_type = component_type
        self.parser_upgrade = parser_upgrade
        self.keywords = [name.lower(), component_type.lower()]

    def examine(self):
        """Return enhanced description for AI components."""
        base_desc = super().examine()
        return f"{base_desc}\n\n[This is a critical AI component: {self.component_type.upper()}]"
