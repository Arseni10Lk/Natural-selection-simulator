import random
import matplotlib.pyplot as plt
from math import radians, cos, sin


class Environment():
    def __init__(self, population_size=10):

        self.population_size = population_size

        # size
        self.length = 1000  # x
        self.width = 500  # y

        # food
        self.food_num = 400

        self.food_pos = []
        self.food_x = []
        self.food_y = []
        for _ in range(0, self.food_num):
            self.food_pos.append([random.randint(0, self.length), random.randint(0, self.width)])
            self.food_x.append(random.randint(0, self.length))
            self.food_y.append(random.randint(0, self.width))

        # population
        self.population = []
        self.create_population()

        # organism positions
        self.organism_pos = []
        self.organism_x = []
        self.organism_y = []
        self.get_organism_positions()

    def create_population(self):

        for _ in range(self.population_size):
            self.population.append(Organism(self))

    def get_organism_positions(self):

        for n in range(self.population_size):
            self.organism_pos.append([self.population[n].x, self.population[n].y])
            self.organism_x.append(self.population[n].x)
            self.organism_y.append(self.population[n].y)

    def update_organism_positions(self):

        [self.population[org_num].move() for org_num in range(self.population_size)]

        self.organism_pos.clear()
        self.organism_x.clear()
        self.organism_y.clear()

        for n in range(self.population_size):
            self.organism_pos.append([self.population[n].x, self.population[n].y])
            self.organism_x.append(self.population[n].x)
            self.organism_y.append(self.population[n].y)

    def plot_environment(self):
        plt.scatter(self.food_x, self.food_y, marker=".", s=1, color="#00C27E")
        plt.scatter(self.organism_x, self.organism_y, color="#FF9A19")
        plt.xlim(0, self.length)
        plt.ylim(0, self.width)
        plt.show()


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

        self.speed = 5
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
        self.direction += random.randint(-1, 1)

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
            if abs(self.env.food_y[food_num] - self.y) <= 1:
                if abs(self.env.food_x[food_num] - self.x) <= 1:

                    self.food += 1
                    # removing it from the map
                    self.env.food_x.remove(self.env.food_x[food_num])
                    self.env.food_y.remove(self.env.food_y[food_num])
                    self.env.food_pos.remove(self.env.food_pos[food_num])

    def move(self):

        for step in range(self.speed):
            # change location
            self.step()
            # forage for food
            self.eat()


new_env = Environment(50)

new_env.update_organism_positions()
new_env.update_organism_positions()
new_env.update_organism_positions()
new_env.update_organism_positions()
new_env.update_organism_positions()
for x in range(50):
    print(new_env.population[x].__dict__)
new_env.plot_environment()
