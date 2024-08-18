import random
from math import radians, cos, sin
from Simulator.visualization import plot_environment, graph_populaiton, Visualisation


class Environment():
    def __init__(self, population_size=10, food_num=100, plot_environment_=True):

        self.population_size = population_size

        # size
        self.length = 500  # x
        self.width = 250  # y

        # food
        self.food_num = food_num

        self.food_pos = []
        self.food_x = []
        self.food_y = []
        self.reset_resources()

        # population
        self.population = []
        self.create_population()

        # organism positions
        self.organism_pos = []
        self.organism_x = []
        self.organism_y = []
        self.get_organism_positions()

        self.generation = 0
        self.day_complete = False

        self.plot_environment_ = plot_environment_
        self.frames = 0
        self.start_time = 0
        self.end_time = 0
        self.population_history = []
        self.population_history.append(population_size)

        self.visualisation = Visualisation(self)

    def create_population(self):

        for _ in range(self.population_size):
            self.population.append(Organism(self))

    def get_organism_positions(self):

        for n in range(self.population_size):
            self.organism_pos.append([self.population[n].x, self.population[n].y])
            self.organism_x.append(self.population[n].x)
            self.organism_y.append(self.population[n].y)

    def update_organism_positions(self):

        [creature.move() for creature in self.population]

        self.organism_pos.clear()
        self.organism_x.clear()
        self.organism_y.clear()

        for n in range(self.population_size):
            self.organism_pos.append([self.population[n].x, self.population[n].y])
            self.organism_x.append(self.population[n].x)
            self.organism_y.append(self.population[n].y)

    def run_day(self, day_length=40):
        for _ in range(day_length):
            self.update_organism_positions()
            if self.plot_environment_:
                self.visualisation.plot_environment(show_framerate=True)
        self.day_complete = True

    def reset_resources(self):

        self.food_pos.clear()
        self.food_x.clear()
        self.food_y.clear()

        for _ in range(self.food_num):
            self.food_pos.append([random.randint(0, self.length), random.randint(0, self.width)])
            self.food_x.append(random.randint(0, self.length))
            self.food_y.append(random.randint(0, self.width))

    def create_new_generation(self):

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
                self.population.append(Organism(self))
                self.population.append(Organism(self))
                self.population_size += 1
            if creature.food == 1:
                self.population.append(Organism(self))

        self.reset_resources()

        self.day_complete = False

    def run_simulation(self, generations_number=20, day_length=20):
        print("Simulation is running ...")
        while self.generation < generations_number:
            print(f"day {self.generation}")
            print(f" initial population {self.population_size}")

            self.run_day(day_length)

            if self.day_complete:
                self.create_new_generation()
                self.population_history.append(self.population_size)
                self.visualisation.graph_population()

            print(f" final population {self.population_size}")


class Organism():
    def __init__(self, env, parent=None):
        self.env = env

        # initial location
        linear_loc = random.randint(0, env.length*2+env.width*2)
        self.x = 0
        self.y = 0
        if linear_loc <= env.length:
            self.x = linear_loc
            self.y = 0
        elif linear_loc <= env.length + env.width:
            self.x = env.length
            self.y = linear_loc - env.length
        elif linear_loc <= env.length*2 + env.width:
            self.x = linear_loc - (env.length + env.width)
            self.y = env.width
        elif linear_loc <= env.length*2 + env.width*2:
            self.x = 0
            self.y = linear_loc - (env.length*2 + env.width)
        else:
            raise Exception("Error while obtaining organism position")

        self.food = 0

        self.speed = 7
        self.size = 5
        self.sense = 20

        # initial direction
        """
        all angles are in degrees,
        measured from the north (positive y) clockwise
        in short, are azimuthal
        """
        if self.x == 0:
            self.direction = random.randint(10, 170)
        elif self.y == 0:
            self.direction = random.choice((random.randint(280, 360), random.randint(0, 80)))
        elif self.x == env.length:
            self.direction = random.randint(190, 350)
        elif self.y == env.width:
            self.direction = random.randint(100, 260)

    def step(self):

        # new location
        self.x += sin(radians(self.direction))
        self.y += cos(radians(self.direction))

        # new direction
        self.direction += random.randint(-10, 10)

        # make sure that nobody can leave the map
        if self.x < 0:
            self.x = 0
        elif self.x > self.env.length:
            self.x = self.env.length

        if self.y < 0:
            self.y = 0
        elif self.y > self.env.width:
            self.y = self.env.width

    def eat(self):

        for food_num in range(len(self.env.food_pos)-1):
            if food_num > len(self.env.food_pos) - 1:
                continue
            if abs(self.env.food_y[food_num] - self.y) <= 7:
                if abs(self.env.food_x[food_num] - self.x) <= 7:

                    self.food += 1
                    # removing it from the map
                    self.env.food_x.pop(food_num)
                    self.env.food_y.pop(food_num)
                    self.env.food_pos.pop(food_num)

    def move(self):

        for step in range(self.speed):
            # change location
            self.step()
            # forage for food
            self.eat()
