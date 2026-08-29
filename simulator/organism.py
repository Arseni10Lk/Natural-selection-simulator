from __future__ import annotations

import random
from math import atan2, cos, degrees, radians, sin, sqrt
from typing import TYPE_CHECKING, Any

from simulator.quadtree import Circle, Rectangle

if TYPE_CHECKING:
    from simulator.environment import Environment


class Organism:
    def __init__(self, env: Environment, brain: Any, parent: Organism | None = None) -> None:
        self.env = env

        self.brain = brain
        self.genome: Any = None
        
        # initial location
        linear_loc = random.randint(0, env.length*2+env.width*2)
        self.x: float = 0
        self.y: float = 0
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
            raise RuntimeError("Error while obtaining organism position")

        self.food: int = 0

        self.speed: float = 0.0
        self.max_speed: float = 7.0
        self.size: float = 7.0
        self.sense: float = 150.0

        # initial direction
        self.direction: float = 0.0
        if self.x == 0:
            self.direction = random.randint(10, 170)
        elif self.y == 0:
            self.direction = random.choice((random.randint(280, 360), random.randint(0, 80)))
        elif self.x == env.length:
            self.direction = random.randint(190, 350)
        elif self.y == env.width:
            self.direction = random.randint(100, 260)

        self.food_found: bool = False
        self.target_direction: float = 0.0
        self.food_distance: float = 2.0

    def think(self) -> None:
        if not self.brain:
            return

        sense_area = Circle(self.x, self.y, self.sense)
        sensed_food = self.env.food_tree.query(sense_area)

        available_food = [f for f in sensed_food if not f.eaten]
        available_food.sort(key=lambda f: (f.x - self.x)**2 + (f.y - self.y)**2)
        closest_five = available_food[:5]
        
        if available_food:
            self.food_distance = sqrt((available_food[0].x - self.x)**2 + (available_food[0].y - self.y)**2)
        else:
            self.food_distance = self.sense
            
        vision_inputs: list[float] = []
        for i in range(5):
            if i < len(closest_five):
                food = closest_five[i]
                
                dist = sqrt((food.x - self.x)**2 + (food.y - self.y)**2)
                angle = degrees(atan2(food.x - self.x, food.y - self.y)) - self.direction
                angle = (angle + 180) % 360 - 180

                normalized_dist = dist / self.sense 
                normalized_angle = angle / 180.0
                
                vision_inputs.extend([normalized_dist, normalized_angle])
            else:
                vision_inputs.extend([2.0, 0.0])
    
        final_neat_inputs = vision_inputs + [self.speed / self.max_speed]
        outputs = self.brain.activate(final_neat_inputs)

        acceleration = outputs[0]
        self.speed += acceleration
        self.speed = max(0.0, min(self.speed, self.max_speed))

        turn_amount = outputs[1] * 40.0
        self.direction += turn_amount
        self.direction %= 360

    def step(self) -> None:
        self.x += sin(radians(self.direction))
        self.y += cos(radians(self.direction))

        if self.x < 0:
            self.x = 0
        elif self.x > self.env.length:
            self.x = self.env.length

        if self.y < 0:
            self.y = 0
        elif self.y > self.env.width:
            self.y = self.env.width

    def eat(self) -> None:
        eat_area = Circle(self.x, self.y, self.size)
        nearby_food = self.env.food_tree.query(eat_area)
        
        for food in nearby_food:
            if not food.eaten:
                if self.env.delayed_food_reset:
                    self.env.consumed_food += 1
                self.food += 1
                self.food_found = False
                food.eaten = True
                break

    def move(self) -> None:
        self.think()
        steps = int(self.speed)
        for _ in range(steps):
            self.step()
            self.eat()

    def look_for_food(self) -> None:
        vision_box = Rectangle(self.x, self.y, self.sense, self.sense)
        nearby_food = self.env.food_tree.query(vision_box)
        
        closest_dist = -1.0
        closest_food = None

        for food in nearby_food:
            if not food.eaten:
                delta_y = food.y - self.y
                delta_x = food.x - self.x
                dist = sqrt(delta_y**2 + delta_x**2)

                if dist <= self.sense and (closest_dist < 0 or dist < closest_dist):
                    closest_dist = dist
                    closest_food = food

        if closest_food:
            delta_y = closest_food.y - self.y
            delta_x = closest_food.x - self.x
            self.target_direction = degrees(atan2(delta_x, delta_y)) % 360
            self.food_distance = closest_dist
            self.food_found = True
