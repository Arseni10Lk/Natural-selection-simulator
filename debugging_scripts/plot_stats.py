import os
import pickle

import matplotlib.pyplot as plt


def main():
    local_dir = os.path.dirname(__file__)
    stats_file = os.path.abspath(os.path.join(local_dir, '..', 'logs', 'evolution_stats.pkl'))
    
    if not os.path.exists(stats_file):
        print(f"Error: {stats_file} not found. Make sure you run the NEAT training first!")
        return

    print("Loading statistics from disk...")
    with open(stats_file, "rb") as f:
        stats = pickle.load(f)

    best_fitness = [c.fitness for c in stats.most_fit_genomes]
    avg_fitness = stats.get_fitness_mean()

    # Extract species histories
    gen_stats = stats.generation_statistics
    
    # Map species_id to a list of (generation, avg_fitness) tuples
    species_history = {}
    
    for gen_idx, species_dict in enumerate(gen_stats):
        for species_id, genome_dict in species_dict.items():
            fitnesses = [fit for fit in genome_dict.values() if fit is not None]
            if not fitnesses:
                continue
                
            avg_species_fitness = sum(fitnesses) / len(fitnesses)
            
            if species_id not in species_history:
                species_history[species_id] = ([], [])
            
            species_history[species_id][0].append(gen_idx)
            species_history[species_id][1].append(avg_species_fitness)

    plt.figure(figsize=(12, 7))
    
    # Get a vibrant colormap with 20 distinct colors
    cmap = plt.get_cmap('tab20')
    
    plotted_species = False
    for species_id, (gens, fits) in species_history.items():
        label = "Species Average" if not plotted_species else None
        line_color = cmap(species_id % 20)
        
        plt.plot(gens, fits, color=line_color, alpha=0.6, linewidth=2, label=label)
        
        
        plt.scatter(gens[0], fits[0], color=line_color, s=20, zorder=5)
        
        plotted_species = True

    plt.plot(best_fitness, label="Overall Champion", color="black", linewidth=4, linestyle="--", zorder=10)
    plt.plot(avg_fitness, label="Total Population Average", color="red", linewidth=4, zorder=10)

    plt.title("NEAT Evolution Progress by Species", fontsize=16)
    plt.xlabel("Generation", fontsize=12)
    plt.ylabel("Average Fitness (Food Eaten)", fontsize=12)
    plt.xlim(0, len(gen_stats))
    plt.grid(True, linestyle="--", alpha=0.6)
    
    # Clean up duplicate labels in the legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), fontsize=12)
    
    print("Graph generated! Close the window to exit.")
    plt.tight_layout()

    plot_path = os.path.join(local_dir, "..", "logs", "evolution_plot.png")
    plt.savefig(plot_path, dpi=300)
    print(f"Graph saved automatically to: {os.path.relpath(plot_path)}")

    plt.show()

if __name__ == "__main__":
    main()
