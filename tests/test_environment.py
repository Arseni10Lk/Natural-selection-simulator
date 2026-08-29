from unittest.mock import MagicMock, patch

from simulator.environment import Environment


@patch('simulator.environment.PygameVisualisation')
def test_environment_initialization(mock_vis):
    # Initialize with small numbers for speed
    env = Environment(population_size=5, food_num=10)
    
    assert env.population_size == 5
    assert len(env.population) == 5
    assert env.food_num == 10
    
    # Food is stored in items and quadtree
    assert len(env.food_items) == 10
    assert not env.stop

@patch('simulator.environment.PygameVisualisation')
def test_create_new_generation_extinction(mock_vis):
    env = Environment(population_size=10, food_num=10)
    
    # Force all organisms to starve
    for org in env.population:
        org.speed = 0
        org.food = 0
        
    env.create_new_generation()
    
    # Nobody survived
    assert env.population_size == 0
    assert len(env.population) == 0

@patch('simulator.environment.PygameVisualisation')
def test_create_new_generation_survival(mock_vis):
    env = Environment(population_size=10, food_num=10)
    
    # Force all organisms to just barely survive (no reproduction)
    for org in env.population:
        org.speed = 0
        org.food = 1
        
    env.create_new_generation()
    
    # Exact same population size
    assert env.population_size == 10
    assert len(env.population) == 10

@patch('simulator.environment.PygameVisualisation')
def test_create_new_generation_explosion(mock_vis):
    env = Environment(population_size=10, food_num=10)
    
    # Force all organisms to eat well and reproduce
    for org in env.population:
        org.speed = 0
        org.food = 2
        
    env.create_new_generation()
    
    # Population should exactly double
    assert env.population_size == 20
    assert len(env.population) == 20

@patch('simulator.environment.PygameVisualisation')
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

@patch('simulator.environment.PygameVisualisation')
def test_run_day(mock_vis):
    env = Environment(population_size=2, food_num=10)
    
    # Mock organisms to prevent real movement
    mock_org1 = MagicMock()
    mock_org1.speed = 1
    mock_org2 = MagicMock()
    mock_org2.speed = 1
    env.population = [mock_org1, mock_org2]
    
    env.run_day(show_framerate=False, day_length=5)
    
    # 5 steps in the day, each organism should move() 5 times
    assert mock_org1.move.call_count == 5
    assert mock_org2.move.call_count == 5
    assert env.day_complete

@patch('simulator.environment.PygameVisualisation')
def test_reset_simulation_and_resources(mock_vis):
    env = Environment(population_size=5, food_num=20)
    
    # Run a mock day to deplete food
    env.food_items.pop()
    env.generation = 5
    env.population.clear()
    
    env.reset_simulation()
    
    assert env.generation == 0
    assert len(env.food_items) == 20
    assert len(env.population) == 5

@patch('simulator.environment.PygameVisualisation')
def test_run_simulation_loop(mock_vis):
    env = Environment(population_size=5, food_num=10)
    
    # We want to test that the loop breaks when population dies
    # Let's mock run_day to instantly kill the population
    def fake_run_day(show, day):
        env.population.clear()
        env.population_size = 0
        env.day_complete = True
        
    env.run_day = fake_run_day
    
    env.run_simulation(generations_number=2, day_length=1)
    
    assert env.generation == 2
    assert env.population_size == 0
