import random
from math import radians, degrees, cos, sin, atan2, sqrt
from Simulator.visualization import MatplotlibVisualisation, PygameVisualisation
from Simulator.quadtree import Point, Rectangle, QuadTree, Circle


class Organism():
    def __init__(self, env, brain, parent=None):
        self.env = env

        self.brain = brain
        
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

        self.speed = 0.0
        self.max_speed = 7
        self.size = 7
        self.sense = 150

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
        self.food_distance = 2.0

    def think(self):
        # We must skip thinking if brain is None (e.g. dummy organisms spawned by env)
        if not self.brain: return

        sense_area = Circle(self.x, self.y, self.sense)
        sensed_food = self.env.food_tree.query(sense_area)

        available_food = [f for f in sensed_food if not f.eaten]
        available_food.sort(key=lambda f: (f.x - self.x)**2 + (f.y - self.y)**2)
        closest_five = available_food[:5]
        if available_food:
            self.food_distance = sqrt((available_food[0].x - self.x)**2 + (available_food[0].y - self.y)**2)
        else:
            self.food_distance = self.sense
        vision_inputs = []
        for i in range(5):
            if i < len(closest_five):
                food = closest_five[i]
                
                # Calculate true distance and relative angle for the neural net
                dist = sqrt((food.x - self.x)**2 + (food.y - self.y)**2)
                # Swap X and Y in atan2 to match the sin/cos movement!
                angle = degrees(atan2(food.x - self.x, food.y - self.y)) - self.direction
                angle = (angle + 180) % 360 - 180  # Wrap around

                normalized_dist = dist / self.sense 
                normalized_angle = angle / 180.0
                
                vision_inputs.extend([normalized_dist, normalized_angle])
            else:
                # padding
                vision_inputs.extend([2.0, 0.0])
    
        final_neat_inputs = vision_inputs + [self.speed / self.max_speed]
        outputs = self.brain.activate(final_neat_inputs)

        acceleration = outputs[0]  # acceleration in range -1 to 1
        self.speed += acceleration
        self.speed = max(0.0, min(self.speed, self.max_speed))

        turn_amount = outputs[1] * 40.0 # max turn of 40 degrees per frame
        self.direction += turn_amount
        self.direction %= 360 # Keep direction between 0 and 360

    def step(self):

        # new location
        self.x += sin(radians(self.direction))
        self.y += cos(radians(self.direction))

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
        eat_area = Circle(self.x, self.y, self.size)
        nearby_food = self.env.food_tree.query(eat_area)
        
        for food in nearby_food:
            if not food.eaten:
                if self.env.delayed_food_reset:
                    self.env.consumed_food += 1
                self.food += 1
                self.food_found = False
                food.eaten = True
                break # Eat one piece at a time if they overlap

    def move(self):

        self.think()

        steps = int(self.speed)

        for _ in range(steps):
            self.step()  # Move 1 pixel
            self.eat()   # Check for food

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
