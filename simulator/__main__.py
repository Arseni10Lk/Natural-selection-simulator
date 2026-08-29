import os
import pickle
from typing import Any

import neat  # type: ignore

from simulator.environment import Environment
from simulator.organism import Organism


def eval_genomes(genomes: list[tuple[int, Any]], config: neat.Config) -> None:
    env = Environment(
        population_size=len(genomes),
        food_num=100,
        multiple_runs=False,
        plot_environment_=False,
        graph_population=False,
        backend="pygame",
        fps_limit=60
    )
    
    env.population.clear()

    for genome_id, genome in genomes:
        genome.fitness = 0.0
        
        brain = neat.nn.FeedForwardNetwork.create(genome, config)
        
        org = Organism(env, brain)
        org.genome = genome

        env.population.append(org) 

    # Run the day directly so we don't trigger create_new_generation
    env.run_day(show_framerate=False, day_length=400)
    
    for org in env.population:
        org.genome.fitness += org.food
        org.genome.fitness += min(0.5, 1 / (org.food_distance + 0.1))

def main() -> None:
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-natural-selection.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_path)

    # Create the NEAT Population
    p = neat.Population(config)

    # Add reporters to see progress in the terminal
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # checkpoint helps also
    p.add_reporter(neat.Checkpointer(50, filename_prefix='logs/checkpoints/checkpoint-'))
    
    print("Starting NEAT Evolution...")
    winner = p.run(eval_genomes, 100)

    print("Saving the Champion...")
    with open("logs/champion_brain.pkl", "wb") as f:
        pickle.dump(winner, f)

    print("Saving the Statistics...")
    with open("logs/evolution_stats.pkl", "wb") as f:
        pickle.dump(stats, f)

if __name__ == "__main__":
    main()
