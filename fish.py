import pygame

class Fish:
    def __init__(self, type, x_pos, y_pos, x_velocity, y_velocity):
        self.type = type
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        if type == "prey":
            self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (0, 0, 255), (6, 6), 6)
        elif type == "predator":
            self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 0, 0), (12, 12), 9)


        