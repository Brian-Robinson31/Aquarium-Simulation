import math

class Food:
    def __init__(self, x_pos, y_pos, fall_speed):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.fall_speed = fall_speed
        
        self.size = 3  
        self.color = (139, 69, 19) 
        
        self.on_ground = False
        self.ground_level = 0
        
        self.time = 0
        self.oscillation_amplitude = 0.5 
        self.oscillation_frequency = 0.15 

    def __update__(self, screen_width, screen_height):
        self.ground_level = screen_height - 5
        
        if not self.on_ground:

            oscillation = math.sin(self.time * self.oscillation_frequency) * self.oscillation_amplitude
            self.x_pos += oscillation
            self.y_pos += self.fall_speed
            self.time += 1
            
            if self.y_pos >= self.ground_level:
                self.y_pos = self.ground_level
                self.on_ground = True
        
        if self.x_pos < 0:
            self.x_pos = 0
        elif self.x_pos > screen_width:
            self.x_pos = screen_width




    
