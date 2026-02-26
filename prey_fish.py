import pygame
from fish import Fish
from boids import Boids

class preyFish(Fish, Boids):
    def __init__(self, x_pos, y_pos, x_velocity, y_velocity):
        Fish.__init__(self, "prey", x_pos, y_pos, x_velocity, y_velocity)
        Boids.__init__(self, x_pos, y_pos, x_velocity, y_velocity)
        self.state = "Default"
    
    def update(self, screen_width, screen_height, predator_list=None, food_list=None, prey_list=None):
        self.hunger_timer += 0.1

        if self.hunger_timer > self.hunger_threshold:
            self.state = "Hungry"

        if self.state == "Default":
            self._move_normal(prey_list)
        elif self.state == "Hungry":
            self._move_hungry(food_list, prey_list)
        

        self._avoid_boundaries(screen_width, screen_height)
        

        if predator_list:
            self._avoid_predators(predator_list)

    def _move_normal(self, prey_list):
        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 255), (6, 6), 6)

        self.boid_step(prey_list)
        
        self.x_pos += self.x_velocity
        self.y_pos += self.y_velocity

    def _move_hungry(self, food_list, prey_list):
        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 255, 255), (6, 6), 6)

        if not food_list:
            self.boid_step(prey_list)
            self.x_pos += self.x_velocity
            self.y_pos += self.y_velocity
            return

        target_food = None
        target_distance = float('inf')
        for food in food_list:
            food_vector = pygame.math.Vector2(food.x_pos - self.x_pos, food.y_pos - self.y_pos)
            distance = food_vector.length()
            if distance < target_distance:
                target_distance = distance
                target_food = food

        if target_food is None:
            self.boid_step(prey_list)
            self.x_pos += self.x_velocity
            self.y_pos += self.y_velocity
            return

        if target_distance < 15:
            food_list.remove(target_food)
            self.state = "Default"
            self.hunger_timer = 0
            self._move_normal(prey_list)
            return

        food_vector = pygame.math.Vector2(target_food.x_pos - self.x_pos, target_food.y_pos - self.y_pos)
        if food_vector.length_squared() > 0:
            food_vector = food_vector.normalize()
            self.x_velocity += food_vector.x * 0.3
            self.y_velocity += food_vector.y * 0.3
            self._limit_velocity(self.max_speed)

        self.x_pos += self.x_velocity
        self.y_pos += self.y_velocity
            

    
    def _avoid_boundaries(self, screen_width, screen_height):

        buffer = 50
        fish_size = 12
        max_speed = 3
        turn_force = 0.1
        

        if self.x_pos < buffer:
            self.x_velocity = min(max_speed, self.x_velocity + turn_force)
        elif self.x_pos + fish_size > screen_width - buffer:
            self.x_velocity = max(-max_speed, self.x_velocity - turn_force)
        

        if self.y_pos < buffer:
            self.y_velocity = min(max_speed, self.y_velocity + turn_force)
        elif self.y_pos + fish_size > screen_height - buffer:
            self.y_velocity = max(-max_speed, self.y_velocity - turn_force)
    
    def _avoid_predators(self, predator_list):
        # TODO: Implement predator avoidance
        pass

        
      