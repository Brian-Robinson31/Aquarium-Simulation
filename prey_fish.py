import pygame
from fish import Fish
from boids import Boids

class preyFish(Fish, Boids):
    def __init__(self, x_pos, y_pos, x_velocity, y_velocity):
        Fish.__init__(self, "prey", x_pos, y_pos, x_velocity, y_velocity)
        Boids.__init__(self, x_pos, y_pos, x_velocity, y_velocity)
        self.state = "Default"
    
    def update(self, screen_width, screen_height, predator_list=None, food_list=None, prey_list=None):
        self.hunger_timer += 0.5

        #if self.hunger_timer > self.hunger_threshold:
            #self.state = "Hungry"

        if self.state == "Default":
            self._move_normal(prey_list)
        elif self.state == "Hungry":
            self._move_hungry(food_list)
        

        self._avoid_boundaries(screen_width, screen_height)
        

        if predator_list:
            self._avoid_predators(predator_list)

    def _move_normal(self, prey_list):
        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 255), (6, 6), 6)

        self.boid_step(prey_list)
        
        self.x_pos += self.x_velocity
        self.y_pos += self.y_velocity

    def _move_hungry(self, food_list):
        # TODO: Implement food-seeking movement

        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        self._move_normal(None)
        pygame.draw.circle(self.image, (0, 100, 255), (6, 6), 6)
        
        pass
    
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

        
      