"""Pygame-based wireframe renderer with retro aesthetics."""

import pygame
import math
from typing import List, Tuple, Optional
from .vector3d import Vector3, Camera, WireframeObject


class RetroRenderer:
    """Renderer for retro vector graphics with CRT-style effects."""

    # Color schemes (RGB tuples)
    COLOR_SCHEMES = {
        'green': {
            'bg': (0, 0, 0),
            'primary': (0, 255, 0),
            'secondary': (0, 180, 0),
            'dim': (0, 100, 0),
            'highlight': (100, 255, 100),
            'glow': (0, 255, 0, 128),
        },
        'amber': {
            'bg': (0, 0, 0),
            'primary': (255, 176, 0),
            'secondary': (200, 140, 0),
            'dim': (100, 70, 0),
            'highlight': (255, 220, 100),
            'glow': (255, 176, 0, 128),
        },
        'blue': {
            'bg': (0, 0, 10),
            'primary': (100, 200, 255),
            'secondary': (50, 150, 255),
            'dim': (30, 100, 180),
            'highlight': (200, 240, 255),
            'glow': (100, 200, 255, 128),
        },
        'white': {
            'bg': (0, 0, 0),
            'primary': (255, 255, 255),
            'secondary': (200, 200, 200),
            'dim': (100, 100, 100),
            'highlight': (255, 255, 255),
            'glow': (255, 255, 255, 128),
        }
    }

    def __init__(self, width: int = 1024, height: int = 768, color_scheme: str = 'green'):
        """
        Initialize the renderer.

        Args:
            width: Window width
            height: Window height
            color_scheme: Color scheme name ('green', 'amber', 'blue', 'white')
        """
        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("SKOOLACH")

        # Set up color scheme
        self.set_color_scheme(color_scheme)

        # Create camera
        self.camera = Camera(width, height, fov=70)

        # Rendering options
        self.draw_glow = True
        self.line_width = 1
        self.glow_width = 3

        # Font for text overlay
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)

        # Animation/effects
        self.time = 0.0
        self.scanline_offset = 0

        # FPS control
        self.clock = pygame.time.Clock()
        self.target_fps = 60

    def set_color_scheme(self, scheme_name: str):
        """Set the active color scheme."""
        if scheme_name in self.COLOR_SCHEMES:
            self.colors = self.COLOR_SCHEMES[scheme_name]
        else:
            self.colors = self.COLOR_SCHEMES['green']

    def clear(self):
        """Clear the screen."""
        self.screen.fill(self.colors['bg'])

    def draw_line(self, p1: Tuple[int, int], p2: Tuple[int, int],
                  color: Optional[Tuple[int, int, int]] = None,
                  width: Optional[int] = None):
        """
        Draw a line with optional glow effect.

        Args:
            p1: Start point (x, y)
            p2: End point (x, y)
            color: RGB color (uses primary if None)
            width: Line width (uses default if None)
        """
        if color is None:
            color = self.colors['primary']
        if width is None:
            width = self.line_width

        # Draw glow effect
        if self.draw_glow and self.glow_width > width:
            glow_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.line(glow_surface, self.colors['glow'], p1, p2, self.glow_width)
            self.screen.blit(glow_surface, (0, 0))

        # Draw main line
        pygame.draw.line(self.screen, color, p1, p2, width)

    def draw_wireframe_object(self, obj: WireframeObject,
                              color: Optional[Tuple[int, int, int]] = None,
                              pulse: bool = False):
        """
        Draw a wireframe object.

        Args:
            obj: The WireframeObject to draw
            color: RGB color (uses primary if None)
            pulse: Whether to apply pulsing effect
        """
        if color is None:
            color = self.colors['primary']

        # Apply pulsing effect to color if requested
        if pulse:
            pulse_amount = (math.sin(self.time * 3) + 1) / 2  # 0 to 1
            color = tuple(int(c * (0.7 + 0.3 * pulse_amount)) for c in color)

        # Get transformed vertices
        vertices = obj.get_transformed_vertices()

        # Project vertices to 2D
        projected = []
        for v in vertices:
            p = self.camera.project(v)
            projected.append(p)

        # Draw edges
        for i, j in obj.edges:
            p1 = projected[i]
            p2 = projected[j]

            # Skip if either vertex is behind camera
            if p1 is None or p2 is None:
                continue

            # Depth-based color variation
            avg_depth = (p1[2] + p2[2]) / 2
            depth_factor = max(0.3, min(1.0, 10.0 / avg_depth))
            depth_color = tuple(int(c * depth_factor) for c in color)

            self.draw_line((p1[0], p1[1]), (p2[0], p2[1]), depth_color)

    def draw_text(self, text: str, position: Tuple[int, int],
                  font_size: str = 'medium',
                  color: Optional[Tuple[int, int, int]] = None,
                  align: str = 'left'):
        """
        Draw text on screen.

        Args:
            text: Text to draw
            position: (x, y) position
            font_size: 'small', 'medium', or 'large'
            color: RGB color (uses primary if None)
            align: 'left', 'center', or 'right'
        """
        if color is None:
            color = self.colors['primary']

        # Select font
        if font_size == 'large':
            font = self.font_large
        elif font_size == 'small':
            font = self.font_small
        else:
            font = self.font_medium

        # Render text
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        # Apply alignment
        if align == 'center':
            text_rect.center = position
        elif align == 'right':
            text_rect.right = position[0]
            text_rect.top = position[1]
        else:  # left
            text_rect.topleft = position

        self.screen.blit(text_surface, text_rect)

    def draw_text_block(self, lines: List[str], position: Tuple[int, int],
                        font_size: str = 'small',
                        line_spacing: int = 5):
        """
        Draw multiple lines of text.

        Args:
            lines: List of text lines
            position: Starting (x, y) position
            font_size: Font size to use
            line_spacing: Extra spacing between lines
        """
        x, y = position
        font = self.font_small if font_size == 'small' else self.font_medium

        for line in lines:
            self.draw_text(line, (x, y), font_size)
            y += font.get_height() + line_spacing

    def draw_box(self, rect: pygame.Rect,
                 color: Optional[Tuple[int, int, int]] = None,
                 fill: bool = False):
        """
        Draw a box/rectangle.

        Args:
            rect: pygame.Rect defining the box
            color: RGB color (uses primary if None)
            fill: Whether to fill the box
        """
        if color is None:
            color = self.colors['primary']

        if fill:
            pygame.draw.rect(self.screen, color, rect)
        else:
            pygame.draw.rect(self.screen, color, rect, 2)

    def draw_scanlines(self, intensity: float = 0.3):
        """
        Draw CRT-style scanlines.

        Args:
            intensity: How dark the scanlines are (0-1)
        """
        scanline_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        for y in range(0, self.height, 2):
            y_offset = (y + self.scanline_offset) % self.height
            alpha = int(255 * intensity)
            pygame.draw.line(scanline_surface, (0, 0, 0, alpha),
                           (0, y_offset), (self.width, y_offset))

        self.screen.blit(scanline_surface, (0, 0))

    def draw_vignette(self, intensity: float = 0.5):
        """
        Draw a vignette effect around the edges.

        Args:
            intensity: How strong the vignette is (0-1)
        """
        vignette_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        center = (self.width // 2, self.height // 2)
        max_radius = math.sqrt(center[0]**2 + center[1]**2)

        # Draw concentric circles with increasing opacity
        steps = 50
        for i in range(steps):
            radius = int(max_radius * (i + 1) / steps)
            alpha = int(255 * intensity * i / steps)
            pygame.draw.circle(vignette_surface, (0, 0, 0, alpha), center, radius)

        self.screen.blit(vignette_surface, (0, 0))

    def update(self, delta_time: float):
        """
        Update renderer state for animations.

        Args:
            delta_time: Time since last frame in seconds
        """
        self.time += delta_time
        self.scanline_offset = int(self.time * 30) % 2

    def present(self):
        """
        Display the rendered frame and handle timing.

        Returns:
            Delta time in seconds since last frame
        """
        pygame.display.flip()
        delta_ms = self.clock.tick(self.target_fps)
        return delta_ms / 1000.0

    def handle_events(self) -> List[pygame.event.Event]:
        """
        Get pygame events.

        Returns:
            List of pygame events
        """
        return pygame.event.get()

    def quit(self):
        """Clean up and quit pygame."""
        pygame.quit()
