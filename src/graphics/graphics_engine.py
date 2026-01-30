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

        # Split the text area into two columns
        self.text_area_split_x = width // 2  # Vertical divider position

        # Left side: Command history
        self.command_history: List[str] = []
        self.max_history_lines = 50

        # Right side: Current description/output
        self.description_lines: List[str] = []
        self.description_scroll = 0  # Scroll offset for long descriptions

        # Status bar
        self.status_text = ""

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

    def add_command(self, command: str):
        """
        Add a command to the history (left side).

        Args:
            command: Command text to add
        """
        self.command_history.append(self.input_prompt + command)

        # Keep only last N lines
        if len(self.command_history) > self.max_history_lines:
            self.command_history = self.command_history[-self.max_history_lines:]

    def set_description(self, text: str):
        """
        Set the description text (right side).

        Args:
            text: Description text (can contain newlines)
        """
        self.description_lines = []
        lines = text.split('\n')

        # Wrap lines to fit in half the screen width
        max_width = 45  # Characters per line for right pane

        for line in lines:
            if len(line) > max_width:
                words = line.split()
                current_line = ""
                for word in words:
                    if len(current_line) + len(word) + 1 <= max_width:
                        current_line += word + " "
                    else:
                        if current_line:
                            self.description_lines.append(current_line.strip())
                        current_line = word + " "
                if current_line:
                    self.description_lines.append(current_line.strip())
            else:
                self.description_lines.append(line)

        # Auto-scroll to show the newest content (bottom of text)
        self._auto_scroll_to_bottom()

    def add_text(self, text: str):
        """
        Add text to the description (appends, doesn't replace).

        Args:
            text: Text to add
        """
        # Split into lines and wrap them
        lines = text.split('\n')
        max_width = 45  # Characters per line for right pane

        for line in lines:
            if len(line) > max_width:
                words = line.split()
                current_line = ""
                for word in words:
                    if len(current_line) + len(word) + 1 <= max_width:
                        current_line += word + " "
                    else:
                        if current_line:
                            self.description_lines.append(current_line.strip())
                        current_line = word + " "
                if current_line:
                    self.description_lines.append(current_line.strip())
            else:
                self.description_lines.append(line)

        # Auto-scroll to show the newest content
        self._auto_scroll_to_bottom()

    def _auto_scroll_to_bottom(self):
        """Automatically scroll to show the most recent text."""
        line_height = 20
        max_desc_lines = int((self.text_area_height - 20) / line_height)

        # Scroll to show the last page of text
        total_lines = len(self.description_lines)
        if total_lines > max_desc_lines:
            self.description_scroll = total_lines - max_desc_lines
        else:
            self.description_scroll = 0

    def set_input_text(self, text: str):
        """Set the current input text."""
        self.input_text = text

    def set_status(self, status_text: str):
        """Set the status bar text."""
        self.status_text = status_text

    def clear_text(self):
        """Clear the text buffers."""
        self.command_history = []
        self.description_lines = []

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
        """Render the split-pane text display area."""
        # Draw top separator line
        separator_y = self.text_area_y - 10
        self.renderer.draw_line(
            (0, separator_y),
            (self.renderer.width, separator_y),
            self.renderer.colors['primary'],
            width=2
        )

        # Draw background for text area
        bg_surface = pygame.Surface((self.renderer.width, self.text_area_height))
        bg_surface.fill((0, 0, 0))
        bg_surface.set_alpha(200)
        self.renderer.screen.blit(bg_surface, (0, self.text_area_y))

        # Draw vertical separator line between panes
        self.renderer.draw_line(
            (self.text_area_split_x, self.text_area_y),
            (self.text_area_split_x, self.renderer.height),
            self.renderer.colors['primary'],
            width=2
        )

        line_height = 20
        input_y = self.renderer.height - 30

        # === STATUS BAR (above left pane) ===
        if self.status_text:
            status_y = self.text_area_y - 30
            self.renderer.draw_text(
                self.status_text,
                (10, status_y),
                font_size='small',
                color=self.renderer.colors['highlight']
            )

        # === LEFT PANE: Command history and input ===
        left_x = 10
        left_width = self.text_area_split_x - 20

        # Calculate available space for history
        available_height = input_y - 10 - (self.text_area_y + 10)
        max_visible_lines = int(available_height / line_height)

        # Render command history (most recent that fit)
        visible_history = self.command_history[-max_visible_lines:] if len(self.command_history) > max_visible_lines else self.command_history

        y = self.text_area_y + 10
        for line in visible_history:
            self.renderer.draw_text(line, (left_x, y), font_size='small')
            y += line_height

        # Draw input line
        input_line = self.input_prompt + self.input_text
        cursor = "_" if int(self.time * 2) % 2 == 0 else " "  # Blinking cursor
        self.renderer.draw_text(
            input_line + cursor,
            (left_x, input_y),
            font_size='medium',
            color=self.renderer.colors['highlight']
        )

        # === RIGHT PANE: Current description/output ===
        right_x = self.text_area_split_x + 10
        right_width = self.renderer.width - self.text_area_split_x - 20

        # Calculate how many description lines fit
        max_desc_lines = int((self.text_area_height - 20) / line_height)

        # Apply scroll offset and render description
        start_line = self.description_scroll
        end_line = start_line + max_desc_lines

        visible_desc = self.description_lines[start_line:end_line]

        y = self.text_area_y + 10
        for line in visible_desc:
            self.renderer.draw_text(line, (right_x, y), font_size='small')
            y += line_height

        # Show scroll indicator if there's more content
        total_lines = len(self.description_lines)
        if total_lines > max_desc_lines:
            scroll_info = f"[{start_line + 1}-{min(end_line, total_lines)}/{total_lines}] Use UP/DOWN to scroll"
            self.renderer.draw_text(
                scroll_info,
                (right_x, self.renderer.height - 50),
                font_size='small',
                color=self.renderer.colors['dim']
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
                        self.add_command(self.input_text)
                        self.input_text = ""

                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]

                elif event.key == pygame.K_DELETE:
                    # Clear the description pane
                    self.description_lines = []
                    self.description_scroll = 0

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

                elif event.key == pygame.K_UP:
                    # Scroll description up
                    if self.description_scroll > 0:
                        self.description_scroll -= 1

                elif event.key == pygame.K_DOWN:
                    # Scroll description down
                    line_height = 20
                    max_desc_lines = int((self.text_area_height - 20) / line_height)
                    max_scroll = max(0, len(self.description_lines) - max_desc_lines)
                    if self.description_scroll < max_scroll:
                        self.description_scroll += 1

                elif event.key == pygame.K_PAGEUP:
                    # Scroll description up by one page
                    line_height = 20
                    max_desc_lines = int((self.text_area_height - 20) / line_height)
                    self.description_scroll = max(0, self.description_scroll - max_desc_lines)

                elif event.key == pygame.K_PAGEDOWN:
                    # Scroll description down by one page
                    line_height = 20
                    max_desc_lines = int((self.text_area_height - 20) / line_height)
                    max_scroll = max(0, len(self.description_lines) - max_desc_lines)
                    self.description_scroll = min(max_scroll, self.description_scroll + max_desc_lines)

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
