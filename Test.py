import pygame
import math

pygame.init()


info = pygame.display.Info()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Aquarium Simulation")
clock = pygame.time.Clock()
arrow = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.polygon(arrow, (0, 0, 255), [(40, 25), (10, 15), (10, 35)])
running = True
x_pos = 100
y_pos = 100
x_velocity = 3
y_velocity = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    x_pos += x_velocity
    y_pos += y_velocity
    

    if x_pos  >= screen.get_width() or x_pos <= 0:
        x_velocity = -x_velocity
    if y_pos  >= screen.get_height() or y_pos <= 0:
        y_velocity = -y_velocity


    angle = math.degrees(math.atan2(-y_velocity, x_velocity))
    rotated_arrow = pygame.transform.rotate(arrow, angle)
    arrow_rect = rotated_arrow.get_rect(center=(x_pos + 25, y_pos + 25))

    screen.fill((100, 100, 255)) 

    screen.blit(rotated_arrow, arrow_rect)


    clock.tick(60)
    pygame.display.flip()
pygame.quit()



