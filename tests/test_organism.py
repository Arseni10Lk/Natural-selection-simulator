import math
from unittest.mock import patch

import pytest

from simulator.organism import Organism
from simulator.quadtree import Point, QuadTree, Rectangle


class MockEnvironment:
    def __init__(self):
        self.length = 500
        self.width = 250
        self.food_tree = QuadTree(Rectangle(250, 125, 250, 125), 4)
        self.delayed_food_reset = False
        self.consumed_food = 0

def test_map_boundaries():
    env = MockEnvironment()
    org = Organism(env, brain=None)
    
    # Force organism out of bounds manually
    org.x = -10
    org.y = 300
    
    # Step should clamp it
    org.direction = 0 # Ensure moving doesn't fix it accidentally via direction, though step adds sin/cos
    org.step()
    
    assert org.x >= 0
    assert org.y <= env.width

def test_trigonometry_atan2():
    env = MockEnvironment()
    org = Organism(env, brain=None)
    org.x = 100
    org.y = 100
    
    # Put food North (Positive Y) -> Should be 0 degrees
    env.food_tree = QuadTree(Rectangle(250, 125, 250, 125), 4)
    env.food_tree.insert(Point(100, 110))
    org.look_for_food()
    assert org.food_found
    assert math.isclose(org.target_direction, 0, abs_tol=0.1)
    
    # Put food East (Positive X) -> Should be 90 degrees
    env.food_tree = QuadTree(Rectangle(250, 125, 250, 125), 4)
    env.food_tree.insert(Point(110, 100))
    org.food_found = False
    org.look_for_food()
    assert math.isclose(org.target_direction, 90, abs_tol=0.1)

    # Put food South (Negative Y) -> Should be 180 degrees
    env.food_tree = QuadTree(Rectangle(250, 125, 250, 125), 4)
    env.food_tree.insert(Point(100, 90))
    org.food_found = False
    org.look_for_food()
    assert math.isclose(org.target_direction, 180, abs_tol=0.1)

    # Put food West (Negative X) -> Should be 270 degrees
    env.food_tree = QuadTree(Rectangle(250, 125, 250, 125), 4)
    env.food_tree.insert(Point(90, 100))
    org.food_found = False
    org.look_for_food()
    assert math.isclose(org.target_direction, 270, abs_tol=0.1)

def test_eating_hitbox_edge_cases():
    env = MockEnvironment()
    org = Organism(env, brain=None)
    org.x = 100
    org.y = 100
    
    # Food exactly 7.0 pixels away (Right on edge) -> Should be eaten
    # 7 pixels East
    food1 = Point(107, 100)
    env.food_tree.insert(food1)
    org.eat()
    assert org.food == 1
    assert food1.eaten
    
    # Food 7.0001 pixels away -> Should be ignored
    food2 = Point(100, 107.0001)
    env.food_tree.insert(food2)
    org.eat()
    # Food count should still be 1 from earlier
    assert org.food == 1
    assert not food2.eaten

def test_tunnel_vision():
    env = MockEnvironment()
    org = Organism(env, brain=None)
    org.x = 100
    org.y = 100
    org.sense = 20
    
    # Food at 21 distance -> outside sense
    food = Point(100, 121)
    env.food_tree.insert(food)
    
    org.look_for_food()
    assert not org.food_found

from unittest.mock import MagicMock


def test_think_with_brain():
    env = MockEnvironment()
    
    # Mock brain that outputs [acceleration, turning]
    mock_brain = MagicMock()
    mock_brain.activate.return_value = [0.5, -0.5]
    
    org = Organism(env, brain=mock_brain)
    org.x = 100
    org.y = 100
    org.speed = 3.0
    org.direction = 90.0
    
    # Add food to be sensed
    env.food_tree.insert(Point(110, 100))
    
    org.think()
    
    # Check if brain was activated
    mock_brain.activate.assert_called_once()
    
    # Check if outputs were applied
    assert org.speed == 3.5  # 3.0 + 0.5
    assert org.direction == 70.0  # 90.0 + (-0.5 * 40.0)

def test_think_no_food():
    env = MockEnvironment()
    
    mock_brain = MagicMock()
    mock_brain.activate.return_value = [0.0, 0.0]
    
    org = Organism(env, brain=mock_brain)
    org.x = 100
    org.y = 100
    
    # No food nearby
    org.think()
    
    mock_brain.activate.assert_called_once()
    # Food distance should default to sense radius
    assert org.food_distance == org.sense

def test_move_updates_position_and_eats():
    env = MockEnvironment()
    
    mock_brain = MagicMock()
    mock_brain.activate.return_value = [0.0, 0.0]
    
    org = Organism(env, brain=mock_brain)
    org.x = 100
    org.y = 100
    org.speed = 2.0  # Should step twice
    org.direction = 0.0 # Moves along Y axis
    
    # Put food in its path
    food = Point(100, 102)
    env.food_tree.insert(food)
    
    org.move()
    
    assert org.food == 1
    assert food.eaten
    assert org.y == 102.0

def test_step_all_boundaries():
    env = MockEnvironment()
    org = Organism(env, brain=None)
    
    # Test Right/Bottom boundaries
    org.x = env.length + 10
    org.y = env.width + 10
    org.direction = 0
    org.step()
    
    assert org.x == env.length
    assert org.y == env.width
    
def test_organism_init_spawn_locations():
    env = MockEnvironment()
    
    
    # Mock randint to test all 4 edges of the map
    with patch('random.randint') as mock_randint:
        # Edge 1: Top
        mock_randint.return_value = 50
        org = Organism(env, brain=None)
        assert org.x == 50 and org.y == 0
        
        # Edge 2: Right
        mock_randint.return_value = env.length + 50
        org = Organism(env, brain=None)
        assert org.x == env.length and org.y == 50
        
        # Edge 3: Bottom
        mock_randint.return_value = env.length + env.width + 50
        org = Organism(env, brain=None)
        assert org.x == 50 and org.y == env.width
        
        # Edge 4: Left
        mock_randint.return_value = env.length*2 + env.width*2 - 50
        org = Organism(env, brain=None)
        assert org.x == 0 and org.y == env.width - 50
        
        # Out of bounds should raise
        mock_randint.return_value = 9999999
        with pytest.raises(RuntimeError):
            Organism(env, brain=None)
