"""Tests for the graphics system."""

import sys
import os
import math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from graphics.vector3d import Vector3, Camera, WireframeObject
from graphics.vector3d import create_cube, create_sphere, create_pyramid


def test_vector3_operations():
    """Test 3D vector operations."""
    v1 = Vector3(1, 2, 3)
    v2 = Vector3(4, 5, 6)

    # Test addition
    v3 = v1 + v2
    assert v3.x == 5 and v3.y == 7 and v3.z == 9

    # Test subtraction
    v4 = v2 - v1
    assert v4.x == 3 and v4.y == 3 and v4.z == 3

    # Test scalar multiplication
    v5 = v1 * 2
    assert v5.x == 2 and v5.y == 4 and v5.z == 6

    print("[PASS]Vector3 operations tests passed")


def test_vector3_rotation():
    """Test vector rotation."""
    v = Vector3(1, 0, 0)

    # Rotate 90 degrees around Y axis
    v_rotated = v.rotate_y(math.pi / 2)

    # After rotating (1,0,0) 90° around Y, should be approximately (0,0,-1)
    assert abs(v_rotated.x) < 0.01  # Close to 0
    assert abs(v_rotated.y) < 0.01  # Still 0
    assert abs(v_rotated.z - (-1)) < 0.01  # Close to -1

    print("[PASS]Vector3 rotation tests passed")


def test_camera_projection():
    """Test camera projection."""
    camera = Camera(800, 600, fov=90)

    # Point in front of camera
    point = Vector3(0, 0, 5)
    result = camera.project(point)

    assert result is not None
    screen_x, screen_y, depth = result

    # Point should be near center of screen
    assert 300 < screen_x < 500
    assert 200 < screen_y < 400

    print("[PASS]Camera projection tests passed")


def test_camera_behind_point():
    """Test camera doesn't project points behind it."""
    camera = Camera(800, 600)

    # Point behind camera
    point = Vector3(0, 0, -10)
    result = camera.project(point)

    # Should return None for points behind camera
    assert result is None

    print("[PASS]Camera behind point tests passed")


def test_wireframe_object_creation():
    """Test wireframe object creation."""
    vertices = [
        Vector3(0, 0, 0),
        Vector3(1, 0, 0),
        Vector3(1, 1, 0),
        Vector3(0, 1, 0),
    ]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]

    obj = WireframeObject(vertices, edges)

    assert len(obj.vertices) == 4
    assert len(obj.edges) == 4
    assert obj.position.x == 0

    print("[PASS]WireframeObject creation tests passed")


def test_wireframe_transformations():
    """Test wireframe transformations."""
    obj = create_cube(2.0)

    # Set position
    obj.position = Vector3(5, 0, 0)
    obj.rotation = Vector3(0, math.pi / 4, 0)
    obj.scale = 2.0

    # Get transformed vertices
    transformed = obj.get_transformed_vertices()

    assert len(transformed) == len(obj.vertices)

    # Check that transformations were applied
    # (exact values depend on transformation order)
    assert transformed[0] != obj.vertices[0]  # Should be different

    print("[PASS]Wireframe transformations tests passed")


def test_create_geometric_shapes():
    """Test predefined shape creation."""
    # Test cube
    cube = create_cube(1.0)
    assert len(cube.vertices) == 8  # Cube has 8 vertices
    assert len(cube.edges) == 12    # Cube has 12 edges

    # Test pyramid
    pyramid = create_pyramid(1.0)
    assert len(pyramid.vertices) == 5  # 4 base + 1 apex
    assert len(pyramid.edges) == 8     # 4 base + 4 sides

    # Test sphere
    sphere = create_sphere(1.0, segments=4)
    assert len(sphere.vertices) > 0
    assert len(sphere.edges) > 0

    print("[PASS]Geometric shapes tests passed")


if __name__ == "__main__":
    test_vector3_operations()
    test_vector3_rotation()
    test_camera_projection()
    test_camera_behind_point()
    test_wireframe_object_creation()
    test_wireframe_transformations()
    test_create_geometric_shapes()
    print("\n[SUCCESS]All graphics tests passed!")
