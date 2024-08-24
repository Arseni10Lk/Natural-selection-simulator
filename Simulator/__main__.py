from Simulator.Simulation import Environment


def main():
    new_env = Environment(50, multiple_runs=True, plot_environment_=False, graph_population=True)
    new_env.run_several_times(20)


if __name__ == "__main__":
    main()
