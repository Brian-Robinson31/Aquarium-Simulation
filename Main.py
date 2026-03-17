import pygame
import math
import random
from prey_fish import preyFish
from predator_fish import PredatorFish
from food import Food;

pygame.init()



info = pygame.display.Info()
screen = pygame.display.set_mode((1500, 600))
pygame.display.set_caption("Aquarium Simulation")
clock = pygame.time.Clock()

# Simulation time: 12 hours pass every 15 real seconds
# At 60 FPS: 12 hours / (15 * 60) = 0.01333 hours per frame
simulation_hours = 0.0  

prey_list = [preyFish(100, 100, 3, 1)]
predator_list = [PredatorFish(400, 300, -2, 2)]

food_list = []
food_spawn_interval = 12  # Food spawns every 12 simulated hours
last_food_spawn = 0


for i in range(30):
    prey_list.append(preyFish(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()), random.choice([-3, -2, -1, 1, 2, 3]), random.choice([-3, -2, -1, 1, 2, 3])))

for i in range(5):
    predator_list.append(PredatorFish(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()), random.choice([-2, -1, 1, 2]), random.choice([-2, -1, 1, 2])))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update simulation time (12 hours per 15 seconds)
    simulation_hours += 12 / (15 * 60)  # 0.01333 hours per frame at 60 FPS
    
    # Spawn food every 12 simulated hours
    if simulation_hours - last_food_spawn >= food_spawn_interval:
        for _ in range(20):  
            food_list.append(Food(random.randint(0, screen.get_width()), random.randint(-20, 0), random.randint(1, 9)))
        last_food_spawn = simulation_hours


    for f in prey_list[:]:
        f.update(screen.get_width(), screen.get_height(), predator_list, food_list, prey_list)

    for f in predator_list[:]:
        f.update(screen.get_width(), screen.get_height(), prey_list, predator_list)

    new_prey = []
    for f in prey_list:
        child = f.reproduce(simulation_hours)
        if child is not None:
            new_prey.append(child)
    if new_prey:
        prey_list.extend(new_prey)

    new_predators = []
    for f in predator_list:
        child = f.reproduce(simulation_hours)
        if child is not None:
            new_predators.append(child)
    if new_predators:
        predator_list.extend(new_predators)

    for f in food_list:
        f.__update__(screen.get_width(), screen.get_height())

    screen.fill((100, 100, 255))
    
    for f in prey_list:
        rect = f.image.get_rect(center=(f.x_pos + 25, f.y_pos + 25))
        screen.blit(f.image, rect)

    for f in predator_list:
        rect = f.image.get_rect(center=(f.x_pos + 25, f.y_pos + 25))
        screen.blit(f.image, rect)

    for f in food_list:
        rect = pygame.Rect(f.x_pos - f.size, f.y_pos - f.size, f.size * 2, f.size * 2)
        pygame.draw.circle(screen, f.color, (int(f.x_pos), int(f.y_pos)), f.size)

    hours = int(simulation_hours) % 24
    minutes = int((simulation_hours % 1) * 60)
    font = pygame.font.Font(None, 36)
    time_text = font.render(f"Time: {hours:02d}:{minutes:02d}", True, (255, 255, 255))
    time_rect = time_text.get_rect(topright=(screen.get_width() - 10, 10))
    screen.blit(time_text, time_rect)

    clock.tick(60)
    pygame.display.flip()
pygame.quit()



