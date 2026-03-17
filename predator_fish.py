import pygame
import math
import random
from fish import Fish

class PredatorFish(Fish):
    def __init__(self, x_pos, y_pos, x_velocity, y_velocity):
        Fish.__init__(self, "predator", x_pos, y_pos, x_velocity, y_velocity)   
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (12, 12), 12)
        self.state = "Default"
        self.reproduction_interval_hours = 72.0  # About 3 simulation days
        self.next_reproduction_time = self.reproduction_interval_hours
        # 6-7 simulation days of additional hunger after becoming Hungry.
        # hunger_timer rises by 0.1667 each frame, and one day is 1800 frames.
        # 6-7 days is about 1800-2100 hunger units.
        self.starvation_day_min = 6
        self.starvation_day_max = 7
        self.starvation_hunger_window = random.uniform(1800, 2100)

    def update(self, screen_width, screen_height, prey_list=None, predator_list=None):
        # Predator gets hungry every 8 simulation hours, which is about 10 seconds in real time
        # At 60 FPS: 100 / (10 * 60) = 0.1667 per frame
        self.hunger_timer += 0.1667

        if self.hunger_timer > self.hunger_threshold + self.starvation_hunger_window:
            if predator_list is not None and self in predator_list:
                predator_list.remove(self)
            return

        if self.hunger_timer > self.hunger_threshold:
            self.state = "Hungry"

        if self.state == "Default":
            self._move_normal()
        elif self.state == "Hungry":
            self._move_hungry(prey_list)

    

        self._avoid_boundaries(screen_width, screen_height)

    def can_reproduce(self, simulation_hours):
        return simulation_hours >= self.next_reproduction_time and self.hunger_timer < self.hunger_threshold

    def reproduce(self, simulation_hours):
        if not self.can_reproduce(simulation_hours):
            return None

        self.next_reproduction_time = simulation_hours + self.reproduction_interval_hours
        child = PredatorFish(
            self.x_pos + random.uniform(-15, 15),
            self.y_pos + random.uniform(-15, 15),
            random.choice([-2, -1, 1, 2]),
            random.choice([-2, -1, 1, 2]),
        )
        child.reproduction_interval_hours = self.reproduction_interval_hours
        child.next_reproduction_time = simulation_hours + child.reproduction_interval_hours
        child.starvation_day_min = self.starvation_day_min
        child.starvation_day_max = self.starvation_day_max
        child.starvation_hunger_window = random.uniform(1800, 2100)
        return child

    def _move_normal(self):
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (12, 12), 12)
        self.x_pos += self.x_velocity
        self.y_pos += self.y_velocity

    def _move_hungry(self, prey_list):

        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)        
        pygame.draw.circle(self.image, (0, 0, 0), (12, 12), 12)
        if not prey_list:
            self.x_pos += self.x_velocity
            self.y_pos += self.y_velocity
            return

        target_prey = None
        target_distance = float('inf')
        for prey in prey_list:
            prey_vector = pygame.math.Vector2(prey.x_pos - self.x_pos, prey.y_pos - self.y_pos)
            distance = prey_vector.length()
            if distance < target_distance:
                target_distance = distance
                target_prey = prey

        if target_prey is None:
            self.x_pos += self.x_velocity
            self.y_pos += self.y_velocity
            return

        if target_distance < 18:
            prey_list.remove(target_prey)
            self.state = "Default"
            self.hunger_timer = 0
            self._move_normal()
            return

        prey_vector = pygame.math.Vector2(target_prey.x_pos - self.x_pos, target_prey.y_pos - self.y_pos)
        if prey_vector.length_squared() == 0:
            self.x_pos += self.x_velocity
            self.y_pos += self.y_velocity
            return

        direction = prey_vector.normalize()
        speed = math.sqrt(self.x_velocity ** 2 + self.y_velocity ** 2)
        self.x_velocity = direction.x * speed
        self.y_velocity = direction.y * speed

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
    

        
        

