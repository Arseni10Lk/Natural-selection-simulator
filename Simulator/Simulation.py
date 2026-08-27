import random
from math import radians, degrees, cos, sin, atan2, sqrt
from Simulator.visualization import MatplotlibVisualisation, PygameVisualisation
from Simulator.quadtree import Point, Rectangle, QuadTree


class Environment():
    def __init__(
            self,
            population_size=10,
            food_num=100,
            multiple_runs=False,
            plot_environment_=True,
            graph_population=True,
            delayed_food_reset=False,
            backend="pygame",
            fps_limit=30
    ):

        self.population_size = population_size
        self.initial_population = population_size

        # size
        self.length = 500  # x
        self.width = 250  # y

        # food
        self.food_num = food_num
        self.initial_food = food_num

        self.food_items = []
        self.food_tree = None
        self.reset_resources()

        self.consumed_food = 0
        self.food_history = [self.food_num]

        # population
        self.population = []
        self.create_population()

        # organism positions
        self.organism_pos = []
        self.organism_x = []
        self.organism_y = []
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
        if self.backend == "matplotlib":
            self.visualisation = MatplotlibVisualisation(self)
        else:
            self.visualisation = PygameVisualisation(self)
        self.stop = False

    def create_population(self):

        for _ in range(self.population_size):
            self.population.append(Organism(self))

    def get_organism_positions(self):

        for n in range(self.population_size):
            self.organism_pos.append([self.population[n].x, self.population[n].y])
            self.organism_x.append(self.population[n].x)
            self.organism_y.append(self.population[n].y)

    def update_organism_positions(self):

        for creature in self.population:
            creature.move()
        
        self.organism_pos.clear()
        self.organism_x.clear()
        self.organism_y.clear()

        for n in range(self.population_size):
            self.organism_pos.append([self.population[n].x, self.population[n].y])
            self.organism_x.append(self.population[n].x)
            self.organism_y.append(self.population[n].y)

    def run_day(self, show_framerate, day_length=40):
        for _ in range(day_length):
            if self.stop:
                self.day_complete = False
                return
            self.update_organism_positions()
            if self.plot_environment_:
                self.visualisation.plot_environment()
                self.visualisation.display_figure(show_framerate=show_framerate)
        self.day_complete = True

    def reset_resources(self):

        self.food_items = []
        self.food_tree = QuadTree(Rectangle(self.length/2, self.width/2, self.length/2, self.width/2), 4)

        for _ in range(self.food_num):
            pt = Point(random.randint(0, self.length), random.randint(0, self.width))
            self.food_items.append(pt)
            self.food_tree.insert(pt)

    def reset_resources_delayed(self):
        self.food_history.append(self.food_num)

        self.food_items = []
        self.food_tree = QuadTree(Rectangle(self.length/2, self.width/2, self.length/2, self.width/2), 4)

        if self.generation == 1:
            new_food_count = (self.food_num
                              - self.consumed_food
                              )
        elif self.generation == 2:
            food_change = 0.4 * self.food_history[self.generation - 1]
            new_food_count = (self.food_num
                              - self.consumed_food
                              + 0.5 * food_change)
        else:
            food_change1 = 0.4 * self.food_history[self.generation - 1]
            food_change2 = 0.4 * self.food_history[self.generation - 2]
            new_food_count = (
                    self.food_num
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

        if self.delayed_food_reset:
            self.reset_resources_delayed()
        else:
            self.reset_resources()

        self.day_complete = False

    def run_simulation(self, show_framerate=False, generations_number=20, day_length=20):
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

    def reset_simulation(self):

        # food
        self.food_items = []
        self.food_tree = None
        self.food_num = self.initial_food
        self.food_history = [self.food_num]
        self.reset_resources()

        # population
        self.population_size = self.initial_population
        self.population = []
        self.create_population()

        # organism positions
        self.organism_pos = []
        self.organism_x = []
        self.organism_y = []
        self.get_organism_positions()

        self.generation = 0
        self.day_complete = False

        self.visualisation.past_population_history.append([self.initial_population])

    def run_several_times(self, times_=20, generations_number=20, day_length=20):
        if not self.stop:
            print("Simulation is running")
            while self.run_num < times_ and not self.stop:
                self.run_simulation(generations_number=generations_number, day_length=day_length)
                if not self.stop:
                    self.reset_simulation()
                self.run_num += 1
                
            if not self.stop and hasattr(self.visualisation, 'show_final_graph'):
                self.visualisation.show_final_graph()


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
        self.size = 7
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

        self.food_found = False
        self.target_direction = 0
        self.food_distance = -1

    def step(self):

        # new location
        self.x += sin(radians(self.direction))
        self.y += cos(radians(self.direction))

        # new direction
        if not self.food_found:
            self.direction += random.randint(-10, 10)
            if self.direction >= 360:
                self.direction = 359
        else:
            turn = self.target_direction - self.direction

            if abs(turn) > 40:
                self.direction += turn/abs(turn)*40
            else:
                self.direction = self.target_direction

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
        eat_box = Rectangle(self.x, self.y, 7, 7)
        nearby_food = self.env.food_tree.query(eat_box)
        
        for food in nearby_food:
            if not food.eaten:
                dist = sqrt((food.x - self.x)**2 + (food.y - self.y)**2)
                if dist <= 7:
                    if self.env.delayed_food_reset:
                        self.env.consumed_food += 1
                    self.food += 1
                    self.food_found = False
                    food.eaten = True
                    break # Eat one piece at a time if they overlap

    def move(self):

        for step in range(self.speed):
            # forage for food
            self.look_for_food()
            # change location
            self.step()
            # consume
            self.eat()

    def look_for_food(self):
        vision_box = Rectangle(self.x, self.y, self.sense, self.sense)
        nearby_food = self.env.food_tree.query(vision_box)
        
        closest_dist = -1
        closest_food = None

        for food in nearby_food:
            if not food.eaten:
                delta_y = food.y - self.y
                delta_x = food.x - self.x
                dist = sqrt(delta_y**2 + delta_x**2)

                if dist <= self.sense:
                    if closest_dist < 0 or dist < closest_dist:
                        closest_dist = dist
                        closest_food = food

        if closest_food:
            delta_y = closest_food.y - self.y
            delta_x = closest_food.x - self.x
            self.target_direction = degrees(atan2(delta_x, delta_y)) % 360
            self.food_distance = closest_dist
            self.food_found = True
