from Simulation import Environment


def main():
    new_env = Environment(50)
    new_env.run_simulation()
    for x in range(new_env.population_size):
        print(new_env.population[x].__dict__)


if __name__ == "__main__":
    main()
