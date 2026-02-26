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


prey_list = [preyFish(100, 100, 3, 1)]
predator_list = [PredatorFish(400, 300, -2, 2)]

food_list = []
food_spawn_interval = 20000 # 
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

    now_ms = pygame.time.get_ticks()
    if now_ms - last_food_spawn >= food_spawn_interval:
        for _ in range(20):  # Spawn 20 food particles at a time
            food_list.append(Food(random.randint(0, screen.get_width()), random.randint(-20, 0), random.randint(1, 9)))
        last_food_spawn = now_ms


    for f in prey_list:
        f.update(screen.get_width(), screen.get_height(), predator_list, food_list, prey_list)

    for f in predator_list:
        f.update(screen.get_width(), screen.get_height(), prey_list)

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



    clock.tick(60)
    pygame.display.flip()
pygame.quit()



