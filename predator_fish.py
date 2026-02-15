import pygame
import math
from fish import Fish

class PredatorFish(Fish):
    def __init__(self, x_pos, y_pos, x_velocity, y_velocity):
        Fish.__init__(self, "predator", x_pos, y_pos, x_velocity, y_velocity)   
        self.state = "Default"

    def update(self, screen_width, screen_height, prey_list=None):
        self.hunger_timer += 0.2
        if self.hunger_timer > self.hunger_threshold:
            self.state = "Hungry"

        if self.state == "Default":
            self._move_normal(prey_list=None)
        elif self.state == "Hungry":
            self._move_hungry(prey_list)

    

        self._avoid_boundaries(screen_width, screen_height)

    def _move_normal(self, prey_list):
        # TODO: Implement boid formation movement

        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (12, 12), 12)
        
        self.x_pos += self.x_velocity
        self.y_pos += self.y_velocity

    def _move_hungry(self, food_list):
        # TODO: Implement food-seeking movement

        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)        
        self._move_normal(None)
        pygame.draw.circle(self.image, (0, 0, 0), (12, 12), 12)
        
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
    

        
        

