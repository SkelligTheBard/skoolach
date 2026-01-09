"""3D vector math for wireframe rendering."""

import math
from typing import Tuple, List


class Vector3:
    """A 3D vector for wireframe geometry."""

    def __init__(self, x: float, y: float, z: float):
        """Initialize a 3D vector."""
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        """Add two vectors."""
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        """Subtract two vectors."""
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        """Multiply by scalar."""
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __repr__(self):
        """String representation."""
        return f"Vector3({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    def rotate_y(self, angle: float):
        """Rotate around Y axis by angle (in radians)."""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector3(
            self.x * cos_a + self.z * sin_a,
            self.y,
            -self.x * sin_a + self.z * cos_a
        )

    def rotate_x(self, angle: float):
        """Rotate around X axis by angle (in radians)."""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector3(
            self.x,
            self.y * cos_a - self.z * sin_a,
            self.y * sin_a + self.z * cos_a
        )

    def rotate_z(self, angle: float):
        """Rotate around Z axis by angle (in radians)."""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector3(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a,
            self.z
        )


class Camera:
    """Simple perspective camera for 3D projection."""

    def __init__(self, width: int, height: int, fov: float = 90):
        """
        Initialize camera.

        Args:
            width: Screen width in pixels
            height: Screen height in pixels
            fov: Field of view in degrees
        """
        self.width = width
        self.height = height
        self.fov = fov
        self.position = Vector3(0, 0, -5)
        self.rotation_y = 0.0  # Yaw

        # Calculate projection parameters
        self.aspect_ratio = width / height
        self.near = 0.1
        self.far = 100.0
        self.scale = 1.0 / math.tan(math.radians(fov / 2))

    def project(self, point: Vector3) -> Tuple[int, int, float]:
        """
        Project a 3D point to 2D screen coordinates.

        Args:
            point: 3D point to project

        Returns:
            Tuple of (screen_x, screen_y, depth)
            Returns None if point is behind camera
        """
        # Transform point relative to camera
        p = point - self.position

        # Apply camera rotation
        p = p.rotate_y(-self.rotation_y)

        # Check if point is behind camera
        if p.z <= self.near:
            return None

        # Perspective projection
        x = p.x / p.z * self.scale * self.height / 2
        y = p.y / p.z * self.scale * self.height / 2

        # Convert to screen coordinates
        screen_x = int(x + self.width / 2)
        screen_y = int(-y + self.height / 2)  # Flip Y axis

        return (screen_x, screen_y, p.z)


class WireframeObject:
    """A 3D wireframe object defined by vertices and edges."""

    def __init__(self, vertices: List[Vector3], edges: List[Tuple[int, int]]):
        """
        Initialize a wireframe object.

        Args:
            vertices: List of 3D vertices
            edges: List of (vertex_index1, vertex_index2) pairs
        """
        self.vertices = vertices
        self.edges = edges
        self.position = Vector3(0, 0, 0)
        self.rotation = Vector3(0, 0, 0)
        self.scale = 1.0

    def get_transformed_vertices(self) -> List[Vector3]:
        """Get vertices after applying transformations."""
        result = []
        for v in self.vertices:
            # Apply scale
            v = v * self.scale

            # Apply rotations
            v = v.rotate_x(self.rotation.x)
            v = v.rotate_y(self.rotation.y)
            v = v.rotate_z(self.rotation.z)

            # Apply translation
            v = v + self.position

            result.append(v)

        return result


# Predefined geometric shapes

def create_cube(size: float = 1.0) -> WireframeObject:
    """Create a wireframe cube."""
    s = size / 2
    vertices = [
        Vector3(-s, -s, -s), Vector3(s, -s, -s), Vector3(s, s, -s), Vector3(-s, s, -s),  # Front
        Vector3(-s, -s, s), Vector3(s, -s, s), Vector3(s, s, s), Vector3(-s, s, s),      # Back
    ]
    edges = [
        # Front face
        (0, 1), (1, 2), (2, 3), (3, 0),
        # Back face
        (4, 5), (5, 6), (6, 7), (7, 4),
        # Connecting edges
        (0, 4), (1, 5), (2, 6), (3, 7),
    ]
    return WireframeObject(vertices, edges)


def create_room_box(width: float = 10, height: float = 5, depth: float = 10) -> WireframeObject:
    """Create a wireframe room (box viewed from inside)."""
    w, h, d = width / 2, height / 2, depth / 2
    vertices = [
        Vector3(-w, -h, -d), Vector3(w, -h, -d), Vector3(w, h, -d), Vector3(-w, h, -d),  # Front wall
        Vector3(-w, -h, d), Vector3(w, -h, d), Vector3(w, h, d), Vector3(-w, h, d),      # Back wall
    ]
    edges = [
        # Front wall
        (0, 1), (1, 2), (2, 3), (3, 0),
        # Back wall
        (4, 5), (5, 6), (6, 7), (7, 4),
        # Side walls
        (0, 4), (1, 5), (2, 6), (3, 7),
    ]
    return WireframeObject(vertices, edges)


def create_pyramid(size: float = 1.0) -> WireframeObject:
    """Create a wireframe pyramid."""
    s = size / 2
    vertices = [
        Vector3(-s, -s, -s), Vector3(s, -s, -s), Vector3(s, -s, s), Vector3(-s, -s, s),  # Base
        Vector3(0, s, 0),  # Apex
    ]
    edges = [
        # Base
        (0, 1), (1, 2), (2, 3), (3, 0),
        # Sides
        (0, 4), (1, 4), (2, 4), (3, 4),
    ]
    return WireframeObject(vertices, edges)


def create_sphere(radius: float = 1.0, segments: int = 8) -> WireframeObject:
    """Create a wireframe sphere."""
    vertices = []
    edges = []

    # Create vertices
    for i in range(segments + 1):
        phi = math.pi * i / segments  # Latitude

        for j in range(segments):
            theta = 2 * math.pi * j / segments  # Longitude

            x = radius * math.sin(phi) * math.cos(theta)
            y = radius * math.cos(phi)
            z = radius * math.sin(phi) * math.sin(theta)

            vertices.append(Vector3(x, y, z))

    # Create edges (latitude lines)
    for i in range(segments):
        for j in range(segments):
            v1 = i * segments + j
            v2 = i * segments + (j + 1) % segments
            edges.append((v1, v2))

    # Create edges (longitude lines)
    for i in range(segments):
        for j in range(segments):
            v1 = i * segments + j
            v2 = ((i + 1) % (segments + 1)) * segments + j
            if i < segments:
                edges.append((v1, v2))

    return WireframeObject(vertices, edges)


def create_torus(major_radius: float = 1.0, minor_radius: float = 0.3, segments: int = 12) -> WireframeObject:
    """Create a wireframe torus (donut)."""
    vertices = []
    edges = []

    for i in range(segments):
        phi = 2 * math.pi * i / segments

        for j in range(segments):
            theta = 2 * math.pi * j / segments

            x = (major_radius + minor_radius * math.cos(theta)) * math.cos(phi)
            y = minor_radius * math.sin(theta)
            z = (major_radius + minor_radius * math.cos(theta)) * math.sin(phi)

            vertices.append(Vector3(x, y, z))

    # Create edges
    for i in range(segments):
        for j in range(segments):
            v1 = i * segments + j
            v2 = i * segments + (j + 1) % segments
            v3 = ((i + 1) % segments) * segments + j

            edges.append((v1, v2))
            edges.append((v1, v3))

    return WireframeObject(vertices, edges)
