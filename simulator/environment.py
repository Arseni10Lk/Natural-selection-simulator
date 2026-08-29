from __future__ import annotations

import random
from typing import Any

from simulator.organism import Organism
from simulator.quadtree import Point, QuadTree, Rectangle
from simulator.visualization import MatplotlibVisualisation, PygameVisualisation


class Environment:
    def __init__(
            self, 
            population_size: int = 10, 
            food_num: int = 100, 
            multiple_runs: bool = False, 
            plot_environment_: bool = True, 
            graph_population: bool = True, 
            delayed_food_reset: bool = False, 
            backend: str = "pygame", 
            fps_limit: int = 30, 
            record: bool = False
    ) -> None:

        self.population_size = population_size
        self.initial_population = population_size

        # size
        self.length = 800  # x
        self.width = 500  # y

        # food
        self.food_num = food_num
        self.initial_food = food_num

        self.food_items: list[Any] = []
        self.food_tree: Any = None
        self.reset_resources()

        self.consumed_food = 0
        self.food_history = [self.food_num]

        # population
        self.population: list[Any] = []
        self.create_population()

        # organism positions
        self.organism_pos: list[Any] = []
        self.organism_x: list[Any] = []
        self.organism_y: list[Any] = []
        self.get_organism_positions()

        self.generation = 0
        self.generations_number = 0
        self.day_complete = False

        self.run_num = 0
        self.multiple_runs = multiple_runs

        self.plot_environment_ = plot_environment_
        self.graph_population = graph_population
        self.delayed_food_reset = delayed_food_reset

        self.backend = backend
        self.fps_limit = fps_limit
        self.record = record
        if self.backend == "matplotlib":
            self.visualisation: Any = MatplotlibVisualisation(self)
        else:
            self.visualisation = PygameVisualisation(self)
        self.stop = False

    def create_population(self) -> None:

        for _ in range(self.population_size):
            self.population.append(Organism(self, brain=None))

    def get_organism_positions(self) -> None:

        for n in range(self.population_size):
            self.organism_pos.append([self.population[n].x, self.population[n].y])
            self.organism_x.append(self.population[n].x)
            self.organism_y.append(self.population[n].y)

    def update_organism_positions(self) -> None:

        for creature in self.population:
            creature.move()
        
        self.organism_pos.clear()
        self.organism_x.clear()
        self.organism_y.clear()

        for n in range(self.population_size):
            self.organism_pos.append([self.population[n].x, self.population[n].y])
            self.organism_x.append(self.population[n].x)
            self.organism_y.append(self.population[n].y)

    def run_day(self, show_framerate: bool = False, day_length: int = 40) -> None:
        for _ in range(day_length):
            if self.stop:
                self.day_complete = False
                return
            self.update_organism_positions()
            if self.plot_environment_:
                self.visualisation.plot_environment()
                self.visualisation.display_figure(show_framerate=show_framerate)
        self.day_complete = True

    def reset_resources(self) -> None:

        self.food_items: list[Any] = []  # type: ignore
        self.food_tree = QuadTree(Rectangle(self.length/2, self.width/2, self.length/2, self.width/2), 4)

        for _ in range(self.food_num):
            pt = Point(random.randint(0, self.length), random.randint(0, self.width))
            self.food_items.append(pt)
            self.food_tree.insert(pt)

    def reset_resources_delayed(self) -> None:
        self.food_history.append(self.food_num)

        self.food_items: list[Any] = []  # type: ignore
        self.food_tree = QuadTree(Rectangle(self.length/2, self.width/2, self.length/2, self.width/2), 4)

        if self.generation == 1:
            new_food_count = (self.food_num
                              - self.consumed_food
                              )
        elif self.generation == 2:
            food_change = 0.4 * self.food_history[self.generation - 1]
            new_food_count = (self.food_num  # type: ignore
                              - self.consumed_food
                              + 0.5 * food_change)
        else:
            food_change1 = 0.4 * self.food_history[self.generation - 1]
            food_change2 = 0.4 * self.food_history[self.generation - 2]
            new_food_count = (
                    self.food_num  # type: ignore
                    - self.consumed_food
                    + 0.5 * food_change1
                    + 0.5 * food_change2
                    )

        self.food_num = round(new_food_count)
        self.consumed_food = 0

        for _ in range(self.food_num):
            pt = Point(random.randint(0, self.length), random.randint(0, self.width))
            self.food_items.append(pt)
            self.food_tree.insert(pt)

    def create_new_generation(self) -> None:

        self.generation += 1

        # identifying survivors
        survivors = []

        for creature in self.population:
            if creature.food >= 1:
                survivors.append(creature)
            if creature.food == 0:
                self.population_size -= 1

        # creating population based on survivors

        self.population.clear()

        for creature in survivors:
            if creature.food >= 2:
                self.population.append(Organism(self, brain=creature.brain))
                self.population.append(Organism(self, brain=creature.brain))
                self.population_size += 1
            if creature.food == 1:
                self.population.append(Organism(self, brain=creature.brain))

        if self.delayed_food_reset:
            self.reset_resources_delayed()
        else:
            self.reset_resources()

        self.day_complete = False

    def run_simulation(self, show_framerate: bool = False, generations_number: int = 20, day_length: int = 20) -> None:
        if not self.stop:
            if not self.multiple_runs:
                print("Simulation is running ...")
            self.generations_number = generations_number
            while self.generation < generations_number:

                if not self.stop:

                    self.run_day(show_framerate, day_length)

                    if self.day_complete:
                        self.create_new_generation()

                        if self.graph_population:
                            self.visualisation.graph_population()

                            if not self.plot_environment_:
                                self.visualisation.display_figure()

                else:
                    return 0
            if not self.multiple_runs and hasattr(self.visualisation, 'show_final_graph'):
                self.visualisation.show_final_graph()
            if hasattr(self.visualisation, 'close'):
                self.visualisation.close()


    def reset_simulation(self) -> None:

        # food
        self.food_items: list[Any] = []  # type: ignore
        self.food_tree: Any = None  # type: ignore
        self.food_num = self.initial_food
        self.food_history = [self.food_num]
        self.reset_resources()

        # population
        self.population_size = self.initial_population
        self.population: list[Any] = []  # type: ignore
        self.create_population()

        # organism positions
        self.organism_pos: list[Any] = []  # type: ignore
        self.organism_x: list[Any] = []  # type: ignore
        self.organism_y: list[Any] = []  # type: ignore
        self.get_organism_positions()

        self.generation = 0
        self.day_complete = False

        self.visualisation.past_population_history.append([self.initial_population])

    def run_several_times(self, times_: int = 20, generations_number: int = 20, day_length: int = 20) -> None:
        if not self.stop:
            print("Simulation is running")
            while self.run_num < times_ and not self.stop:
                self.run_simulation(generations_number=generations_number, day_length=day_length)
                if not self.stop:
                    self.reset_simulation()
                self.run_num += 1
                
            if not self.stop and hasattr(self.visualisation, 'show_final_graph'):
                self.visualisation.show_final_graph()


