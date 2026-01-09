"""Scene management for visualizing rooms and items."""

import math
import random
from typing import Dict, List, Optional
from .vector3d import (Vector3, WireframeObject, create_cube, create_pyramid,
                       create_sphere, create_room_box, create_torus)


class ItemVisual:
    """Visual representation of a game item."""

    def __init__(self, name: str, wireframe: WireframeObject,
                 position: Vector3, is_ai_component: bool = False):
        """
        Initialize item visual.

        Args:
            name: Item name
            wireframe: The 3D wireframe object
            position: Position in the room
            is_ai_component: Whether this is an AI component (special effects)
        """
        self.name = name
        self.wireframe = wireframe
        self.position = position
        self.is_ai_component = is_ai_component
        self.rotation_speed = Vector3(
            random.uniform(-0.5, 0.5),
            random.uniform(0.5, 1.5),
            random.uniform(-0.5, 0.5)
        )
        self.bob_offset = random.uniform(0, math.pi * 2)
        self.bob_speed = random.uniform(1.0, 2.0)

    def update(self, time: float):
        """
        Update item animation.

        Args:
            time: Current game time
        """
        # Apply rotation
        self.wireframe.rotation = Vector3(
            self.rotation_speed.x * time,
            self.rotation_speed.y * time,
            self.rotation_speed.z * time
        )

        # Apply bobbing motion
        bob = math.sin(time * self.bob_speed + self.bob_offset) * 0.2
        self.wireframe.position = Vector3(
            self.position.x,
            self.position.y + bob,
            self.position.z
        )


class RoomScene:
    """3D scene representation of a game room."""

    def __init__(self, room_name: str):
        """
        Initialize room scene.

        Args:
            room_name: Name of the room
        """
        self.room_name = room_name
        self.room_wireframe = None
        self.items: List[ItemVisual] = []
        self.particles: List['Particle'] = []
        self.ambient_objects: List[WireframeObject] = []

        # Create room-specific geometry
        self._setup_room_geometry()

    def _setup_room_geometry(self):
        """Set up the 3D geometry specific to this room."""
        # Default room box
        self.room_wireframe = create_room_box(12, 6, 12)

        # Add room-specific decorations based on room name
        if "crash" in self.room_name.lower():
            self._setup_crash_site()
        elif "memory" in self.room_name.lower():
            self._setup_memory_corridor()
        elif "tokenizer" in self.room_name.lower():
            self._setup_tokenizer_chamber()
        elif "archive" in self.room_name.lower():
            self._setup_archives()
        elif "embedding" in self.room_name.lower():
            self._setup_embedding_space()
        elif "virus" in self.room_name.lower():
            self._setup_virus_lair()

    def _setup_crash_site(self):
        """Set up crash site geometry."""
        # Scattered debris - random cubes
        for _ in range(5):
            debris = create_cube(random.uniform(0.3, 0.8))
            debris.position = Vector3(
                random.uniform(-4, 4),
                random.uniform(-2, 0),
                random.uniform(-4, 4)
            )
            debris.rotation = Vector3(
                random.uniform(0, math.pi),
                random.uniform(0, math.pi),
                random.uniform(0, math.pi)
            )
            self.ambient_objects.append(debris)

    def _setup_memory_corridor(self):
        """Set up memory corridor geometry."""
        # Data stream lines
        for i in range(4):
            # Vertical data streams
            stream = WireframeObject(
                vertices=[
                    Vector3(-5 + i * 3, -3, -5 + j * 2)
                    for j in range(6)
                ],
                edges=[(j, j + 1) for j in range(5)]
            )
            self.ambient_objects.append(stream)

    def _setup_tokenizer_chamber(self):
        """Set up tokenizer chamber geometry."""
        # Floating text fragments (represented as small cubes)
        for _ in range(10):
            fragment = create_cube(0.2)
            fragment.position = Vector3(
                random.uniform(-4, 4),
                random.uniform(-1, 2),
                random.uniform(-4, 4)
            )
            self.ambient_objects.append(fragment)

        # Pedestal in center
        pedestal = create_pyramid(1.5)
        pedestal.position = Vector3(0, -2, 2)
        self.ambient_objects.append(pedestal)

    def _setup_archives(self):
        """Set up archives geometry."""
        # Book shelves (represented as boxes)
        for i in range(-2, 3):
            shelf = create_cube(1.0)
            shelf.position = Vector3(i * 2.5, 0, 5)
            shelf.scale = 2.0
            self.ambient_objects.append(shelf)

    def _setup_embedding_space(self):
        """Set up embedding space geometry."""
        # Multiple floating spheres representing word vectors
        for _ in range(8):
            sphere = create_sphere(0.3, segments=6)
            sphere.position = Vector3(
                random.uniform(-4, 4),
                random.uniform(-2, 2),
                random.uniform(-4, 4)
            )
            self.ambient_objects.append(sphere)

    def _setup_virus_lair(self):
        """Set up virus lair geometry."""
        # Corrupted geometry - jagged shapes
        for _ in range(6):
            corrupt = create_pyramid(random.uniform(0.5, 1.5))
            corrupt.position = Vector3(
                random.uniform(-5, 5),
                random.uniform(-2, 1),
                random.uniform(-5, 5)
            )
            corrupt.rotation = Vector3(
                random.uniform(0, math.pi * 2),
                random.uniform(0, math.pi * 2),
                random.uniform(0, math.pi * 2)
            )
            self.ambient_objects.append(corrupt)

    def add_item(self, item_name: str, is_ai_component: bool = False):
        """
        Add an item to the scene.

        Args:
            item_name: Name of the item
            is_ai_component: Whether this is an AI component
        """
        # Choose appropriate geometry for the item
        wireframe = self._get_item_geometry(item_name, is_ai_component)

        # Position items in a circle around the room
        angle = len(self.items) * (2 * math.pi / 5)  # Space items out
        radius = 3
        position = Vector3(
            math.cos(angle) * radius,
            0,
            math.sin(angle) * radius
        )

        item_visual = ItemVisual(item_name, wireframe, position, is_ai_component)
        self.items.append(item_visual)

    def _get_item_geometry(self, item_name: str, is_ai_component: bool) -> WireframeObject:
        """
        Get appropriate geometry for an item.

        Args:
            item_name: Name of the item
            is_ai_component: Whether this is an AI component

        Returns:
            WireframeObject for the item
        """
        name_lower = item_name.lower()

        if is_ai_component:
            # AI components get special geometry
            if "tokenizer" in name_lower:
                return create_cube(0.8)
            elif "embedding" in name_lower:
                return create_sphere(0.8, segments=8)
            elif "attention" in name_lower:
                return create_torus(0.6, 0.2, segments=12)
            else:
                return create_torus(0.5, 0.15, segments=10)

        # Regular items
        if "key" in name_lower:
            return create_cube(0.3)
        elif "book" in name_lower or "codex" in name_lower:
            return create_cube(0.6)
        elif "light" in name_lower or "flashlight" in name_lower:
            return create_pyramid(0.4)
        else:
            return create_cube(0.5)

    def remove_item(self, item_name: str):
        """Remove an item from the scene."""
        self.items = [item for item in self.items if item.name != item_name]

    def update(self, time: float):
        """
        Update scene animations.

        Args:
            time: Current game time
        """
        # Update item animations
        for item in self.items:
            item.update(time)

        # Slowly rotate ambient objects
        for obj in self.ambient_objects:
            obj.rotation = Vector3(
                obj.rotation.x + 0.001,
                obj.rotation.y + 0.002,
                obj.rotation.z + 0.001
            )


class SceneManager:
    """Manages scenes for all rooms in the game."""

    def __init__(self):
        """Initialize scene manager."""
        self.scenes: Dict[str, RoomScene] = {}
        self.current_scene: Optional[RoomScene] = None

    def create_scene(self, room_name: str, items: List[str],
                     ai_components: List[str]) -> RoomScene:
        """
        Create or get a scene for a room.

        Args:
            room_name: Name of the room
            items: List of item names in the room
            ai_components: List of AI component names in the room

        Returns:
            The RoomScene for this room
        """
        if room_name not in self.scenes:
            scene = RoomScene(room_name)

            # Add items to scene
            for item_name in items:
                is_ai = item_name in ai_components
                scene.add_item(item_name, is_ai)

            self.scenes[room_name] = scene

        return self.scenes[room_name]

    def get_scene(self, room_name: str) -> Optional[RoomScene]:
        """Get the scene for a room."""
        return self.scenes.get(room_name)

    def update_scene_items(self, room_name: str, items: List[str],
                          ai_components: List[str]):
        """
        Update items in a scene.

        Args:
            room_name: Name of the room
            items: Current list of item names
            ai_components: List of AI component names
        """
        scene = self.get_scene(room_name)
        if not scene:
            return

        # Remove items no longer in room
        current_item_names = [item.name for item in scene.items]
        for item_name in current_item_names:
            if item_name not in items:
                scene.remove_item(item_name)

        # Add new items
        for item_name in items:
            if item_name not in current_item_names:
                is_ai = item_name in ai_components
                scene.add_item(item_name, is_ai)
