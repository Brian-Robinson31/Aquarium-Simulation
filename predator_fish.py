import pygame
import math
from fish import Fish

class PredatorFish(Fish):
    def __init__(self, x_pos, y_pos, x_velocity, y_velocity):
        Fish.__init__(self, "predator", x_pos, y_pos, x_velocity, y_velocity)   
    def update(self, screen_width, screen_height):
        self.x_pos += self.x_velocity
        self.y_pos += self.y_velocity
        
        if self.x_pos >= screen_width or self.x_pos <= 2:
            self.x_velocity = -self.x_velocity
        if self.y_pos >= screen_height or self.y_pos <= 2:
            self.y_velocity = -self.y_velocity


