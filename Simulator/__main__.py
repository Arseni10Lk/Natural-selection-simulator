from Simulator.Simulation import Environment

def main():
    # Example 1: Use Pygame for fast, live visualization of the ecosystem
    new_env = Environment(
        50, 
        multiple_runs=True, 
        plot_environment_=True, 
        graph_population=True, 
        backend="pygame",
        fps_limit=60
    )
    new_env.run_several_times(2)

if __name__ == "__main__":
    main()
