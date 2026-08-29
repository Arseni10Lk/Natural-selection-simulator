import math

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
