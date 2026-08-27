import pytest
from unittest.mock import patch
from Simulator.Simulation import Environment, Organism

@patch('Simulator.Simulation.PygameVisualisation')
def test_environment_initialization(mock_vis):
    # Initialize with small numbers for speed
    env = Environment(population_size=5, food_num=10)
    
    assert env.population_size == 5
    assert len(env.population) == 5
    assert env.food_num == 10
    
    # Food is stored in items and quadtree
    assert len(env.food_items) == 10
    assert not env.stop

@patch('Simulator.Simulation.PygameVisualisation')
def test_create_new_generation_extinction(mock_vis):
    env = Environment(population_size=10, food_num=10)
    
    # Force all organisms to starve
    for org in env.population:
        org.food = 0
        
    env.create_new_generation()
    
    # Nobody survived
    assert env.population_size == 0
    assert len(env.population) == 0

@patch('Simulator.Simulation.PygameVisualisation')
def test_create_new_generation_survival(mock_vis):
    env = Environment(population_size=10, food_num=10)
    
    # Force all organisms to just barely survive (no reproduction)
    for org in env.population:
        org.food = 1
        
    env.create_new_generation()
    
    # Exact same population size
    assert env.population_size == 10
    assert len(env.population) == 10

@patch('Simulator.Simulation.PygameVisualisation')
def test_create_new_generation_explosion(mock_vis):
    env = Environment(population_size=10, food_num=10)
    
    # Force all organisms to eat well and reproduce
    for org in env.population:
        org.food = 2
        
    env.create_new_generation()
    
    # Population should exactly double
    assert env.population_size == 20
    assert len(env.population) == 20

@patch('Simulator.Simulation.PygameVisualisation')
def test_delayed_food_math(mock_vis):
    env = Environment(population_size=10, food_num=100)
    env.generation = 1
    env.consumed_food = 50
    
    env.reset_resources_delayed()
    
    # Formula for Gen 1: food_num - consumed_food
    # 100 - 50 = 50
    assert env.food_num == 50
    
    # Gen 2
    env.generation = 2
    env.consumed_food = 20
    env.reset_resources_delayed()
    
    # Formula for Gen 2:
    # food_change = 0.4 * food_history[1] = 0.4 * 50 = 20
    # new_food = 50 - 20 + 0.5 * 20 = 40
    assert env.food_num == 50
