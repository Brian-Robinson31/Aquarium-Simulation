import pygame
import math
from prey_fish import preyFish

class Boids:
    def __init__(self, x_pos, y_pos, x_velocity, y_velocity, perception_radius):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.perception_radius = perception_radius

      