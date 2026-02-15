import pygame

class Fish:
    def __init__(self, type, x_pos, y_pos, x_velocity, y_velocity):
        self.type = type
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.state = "Default"
        self.hunger_timer = 0
        self.hunger_threshold = 100



        