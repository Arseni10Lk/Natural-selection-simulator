from Simulator.Simulation import Environment


def main():
    new_env = Environment(50, graph_population=True)
    new_env.run_simulation(show_framerate=True)


if __name__ == "__main__":
    main()
