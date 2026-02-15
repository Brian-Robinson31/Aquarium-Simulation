import pygame
import math
import random
from prey_fish import preyFish
from predator_fish import PredatorFish

pygame.init()



info = pygame.display.Info()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Aquarium Simulation")
clock = pygame.time.Clock()
prey_list = [preyFish(100, 100, 3, 1)]
predator_list = [PredatorFish(400, 300, -2, 2)]


for int in range(30):
    prey_list.append(preyFish(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()), random.randint(-3, 3), random.randint(-3, 3)))

for int in range(5):
    predator_list.append(PredatorFish(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()), random.randint(-2, 2), random.randint(-2, 2)))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    for f in prey_list:
        f.update(screen.get_width(), screen.get_height(), predator_list, None, prey_list)

    for f in predator_list:
        f.update(screen.get_width(), screen.get_height())

    screen.fill((100, 100, 255))
    
    for f in prey_list:
        rect = f.image.get_rect(center=(f.x_pos + 25, f.y_pos + 25))
        screen.blit(f.image, rect)

    for f in predator_list:
        rect = f.image.get_rect(center=(f.x_pos + 25, f.y_pos + 25))
        screen.blit(f.image, rect)

    
    clock.tick(60)
    pygame.display.flip()
pygame.quit()



