"""Graphics engine that integrates rendering with the game."""

import pygame
import math
from typing import Optional, List, Tuple
from .renderer import RetroRenderer
from .scene import SceneManager, RoomScene
from .vector3d import Vector3


class GraphicsEngine:
    """Main graphics engine that handles rendering the game world."""

    def __init__(self, width: int = 1024, height: int = 768,
                 color_scheme: str = 'green', use_effects: bool = True):
        """
        Initialize graphics engine.

        Args:
            width: Window width
            height: Window height
            color_scheme: Color scheme ('green', 'amber', 'blue', 'white')
            use_effects: Whether to use CRT effects (scanlines, etc.)
        """
        self.renderer = RetroRenderer(width, height, color_scheme)
        self.scene_manager = SceneManager()
        self.current_scene: Optional[RoomScene] = None
        self.use_effects = use_effects

        # Text display area (bottom portion of screen)
        self.text_area_height = 250
        self.text_area_y = height - self.text_area_height

        # Text buffer for displaying game messages
        self.text_lines: List[str] = []
        self.max_text_lines = 10

        # Input area
        self.input_text = ""
        self.input_prompt = "> "

        # Camera control
        self.camera_rotation = 0.0
        self.camera_rotation_speed = 0.3
        self.auto_rotate = True

        # Animation time
        self.time = 0.0

    def set_current_room(self, room_name: str, items: List[str],
                        ai_components: List[str]):
        """
        Set the current room to display.

        Args:
            room_name: Name of the room
            items: List of item names in the room
            ai_components: List of AI component names
        """
        # Create or get scene
        scene = self.scene_manager.create_scene(room_name, items, ai_components)
        self.current_scene = scene
        self.scene_manager.current_scene = scene

    def update_room_items(self, room_name: str, items: List[str],
                         ai_components: List[str]):
        """
        Update items in the current room.

        Args:
            room_name: Name of the room
            items: Current list of items
            ai_components: List of AI component names
        """
        self.scene_manager.update_scene_items(room_name, items, ai_components)

    def add_text(self, text: str):
        """
        Add text to the display buffer.

        Args:
            text: Text to add (can contain newlines)
        """
        lines = text.split('\n')
        for line in lines:
            # Wrap long lines
            if len(line) > 80:
                words = line.split()
                current_line = ""
                for word in words:
                    if len(current_line) + len(word) + 1 <= 80:
                        current_line += word + " "
                    else:
                        self.text_lines.append(current_line.strip())
                        current_line = word + " "
                if current_line:
                    self.text_lines.append(current_line.strip())
            else:
                self.text_lines.append(line)

        # Keep only last N lines
        if len(self.text_lines) > self.max_text_lines:
            self.text_lines = self.text_lines[-self.max_text_lines:]

    def set_input_text(self, text: str):
        """Set the current input text."""
        self.input_text = text

    def clear_text(self):
        """Clear the text buffer."""
        self.text_lines = []

    def render(self):
        """Render the current frame."""
        # Clear screen
        self.renderer.clear()

        # Render 3D scene if we have one
        if self.current_scene:
            self._render_3d_scene()

        # Draw text overlay
        self._render_text_overlay()

        # Apply retro effects
        if self.use_effects:
            self.renderer.draw_scanlines(intensity=0.15)
            # self.renderer.draw_vignette(intensity=0.2)  # Optional

        # Present frame
        delta_time = self.renderer.present()
        return delta_time

    def _render_3d_scene(self):
        """Render the 3D wireframe scene."""
        # Update camera rotation
        if self.auto_rotate:
            self.camera_rotation += self.camera_rotation_speed * 0.016  # Assuming ~60fps

        self.renderer.camera.rotation_y = self.camera_rotation

        # Update scene animations
        self.current_scene.update(self.time)

        # Draw room wireframe
        if self.current_scene.room_wireframe:
            self.renderer.draw_wireframe_object(
                self.current_scene.room_wireframe,
                color=self.renderer.colors['dim']
            )

        # Draw ambient objects
        for obj in self.current_scene.ambient_objects:
            self.renderer.draw_wireframe_object(
                obj,
                color=self.renderer.colors['secondary']
            )

        # Draw items
        for item in self.current_scene.items:
            color = self.renderer.colors['highlight'] if item.is_ai_component else self.renderer.colors['primary']
            self.renderer.draw_wireframe_object(
                item.wireframe,
                color=color,
                pulse=item.is_ai_component
            )

    def _render_text_overlay(self):
        """Render the text display area."""
        # Draw separator line
        separator_y = self.text_area_y - 10
        self.renderer.draw_line(
            (0, separator_y),
            (self.renderer.width, separator_y),
            self.renderer.colors['primary'],
            width=2
        )

        # Draw background for text area
        text_rect = pygame.Rect(0, self.text_area_y, self.renderer.width, self.text_area_height)
        bg_surface = pygame.Surface((self.renderer.width, self.text_area_height))
        bg_surface.fill((0, 0, 0))
        bg_surface.set_alpha(200)
        self.renderer.screen.blit(bg_surface, (0, self.text_area_y))

        # Draw text lines
        y = self.text_area_y + 10
        for line in self.text_lines:
            self.renderer.draw_text(line, (10, y), font_size='small')
            y += 20

        # Draw input line
        input_y = self.renderer.height - 30
        input_line = self.input_prompt + self.input_text
        cursor = "_" if int(self.time * 2) % 2 == 0 else " "  # Blinking cursor
        self.renderer.draw_text(
            input_line + cursor,
            (10, input_y),
            font_size='medium',
            color=self.renderer.colors['highlight']
        )

    def handle_input(self) -> Tuple[Optional[str], bool]:
        """
        Handle input events.

        Returns:
            Tuple of (command_string or None, should_quit)
        """
        command = None
        should_quit = False

        for event in self.renderer.handle_events():
            if event.type == pygame.QUIT:
                should_quit = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    should_quit = True

                elif event.key == pygame.K_RETURN:
                    # Submit command
                    if self.input_text:
                        command = self.input_text
                        self.add_text(self.input_prompt + self.input_text)
                        self.input_text = ""

                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]

                elif event.key == pygame.K_TAB:
                    # Toggle auto-rotate
                    self.auto_rotate = not self.auto_rotate

                elif event.key == pygame.K_LEFT:
                    # Manual camera rotation
                    self.camera_rotation -= 0.1
                    self.auto_rotate = False

                elif event.key == pygame.K_RIGHT:
                    # Manual camera rotation
                    self.camera_rotation += 0.1
                    self.auto_rotate = False

                elif event.unicode and event.unicode.isprintable():
                    self.input_text += event.unicode

        return command, should_quit

    def update(self, delta_time: float):
        """
        Update graphics engine state.

        Args:
            delta_time: Time since last update in seconds
        """
        self.time += delta_time
        self.renderer.update(delta_time)

    def quit(self):
        """Clean up and quit graphics."""
        self.renderer.quit()

    def set_color_scheme(self, scheme: str):
        """
        Change the color scheme.

        Args:
            scheme: Color scheme name
        """
        self.renderer.set_color_scheme(scheme)

    def toggle_effects(self):
        """Toggle CRT effects on/off."""
        self.use_effects = not self.use_effects
