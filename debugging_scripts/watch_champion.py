import os
import pickle
import sys

import neat  # type: ignore

# Add root directory to sys.path so we can import simulator
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from simulator.environment import Environment
from simulator.organism import Organism


def main():
    # Point to the config in the simulator folder
    local_dir = os.path.dirname(__file__)
    config_path = os.path.abspath(os.path.join(local_dir, '..', 'simulator', 'config-natural-selection.txt'))
    
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # Point to logs which are in the root directory
    logs_dir = os.path.abspath(os.path.join(local_dir, '..', 'logs'))
    brain_path = os.path.join(logs_dir, 'champion_brain.pkl')

    if not os.path.exists(brain_path):
        print(f"Error: {brain_path} not found!")
        return

    with open(brain_path, "rb") as f:
        winner = pickle.load(f)

    print("Loaded champion! Starting Sandbox Simulation...")

    env = Environment(
        population_size=10,
        food_num=200,       
        multiple_runs=False,
        plot_environment_=True,
        graph_population=True,
        backend="pygame",
        delayed_food_reset=True,
        fps_limit=20,
        record=False,
    )
    
    env.population.clear()

    champion_brain = neat.nn.FeedForwardNetwork.create(winner, config)
    
    for _ in range(10):
        org = Organism(env, champion_brain)
        env.population.append(org)

    env.population_size = 10

    env.run_simulation(day_length=50)

if __name__ == "__main__":
    main()
