import argparse
import csv
import pygame
import math
import random
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from prey_fish import preyFish
from predator_fish import PredatorFish
from food import Food;


parser = argparse.ArgumentParser(description="Aquarium predator-prey simulation")
parser.add_argument(
    "--starting-prey",
    type=int,
    default=31,
    help="Number of prey fish at simulation start (default: 31)",
)
parser.add_argument(
    "--starting-predators",
    type=int,
    default=6,
    help="Number of predator fish at simulation start (default: 6)",
)
parser.add_argument(
    "--food-spawn-count",
    type=int,
    default=20,
    help="Number of food pellets spawned each food cycle (default: 20)",
)
parser.add_argument(
    "--food-spawn-frequency",
    type=float,
    default=12.0,
    help="Food spawn frequency in simulated hours (default: 12)",
)
parser.add_argument(
    "--csv-output",
    default="",
    help="CSV output path. If omitted, a timestamped file is created per run.",
)
args = parser.parse_args()

if args.starting_prey < 0:
    parser.error("--starting-prey must be 0 or greater")
if args.starting_predators < 0:
    parser.error("--starting-predators must be 0 or greater")
if args.food_spawn_count < 0:
    parser.error("--food-spawn-count must be 0 or greater")
if args.food_spawn_frequency <= 0:
    parser.error("--food-spawn-frequency must be greater than 0")

pygame.init()



info = pygame.display.Info()
screen = pygame.display.set_mode((1500, 600))
pygame.display.set_caption("Aquarium Simulation")
clock = pygame.time.Clock()

# Simulation time: 12 hours pass every 15 real seconds
# At 60 FPS: 12 hours / (15 * 60) = 0.01333 hours per frame
simulation_hours = 0.0  

prey_list = []
predator_list = []

food_list = []
food_spawn_interval = args.food_spawn_frequency
food_spawn_count = args.food_spawn_count
last_food_spawn = 0


for i in range(args.starting_prey):
    prey_list.append(preyFish(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()), random.choice([-3, -2, -1, 1, 2, 3]), random.choice([-3, -2, -1, 1, 2, 3])))

for i in range(args.starting_predators):
    predator_list.append(PredatorFish(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()), random.choice([-2, -1, 1, 2]), random.choice([-2, -1, 1, 2])))

running = True
all_fish_dead = False
fast_forward_enabled = False

normal_steps_per_frame = 1
fast_steps_per_frame = 10

font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 28)
button_rect = pygame.Rect(10, 10, 220, 44)

time_history = [simulation_hours]
prey_population_history = [len(prey_list)]
predator_population_history = [len(predator_list)]
food_population_history = [len(food_list)]
last_logged_hour = int(simulation_hours)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect.collidepoint(event.pos):
                fast_forward_enabled = not fast_forward_enabled

    steps_this_frame = fast_steps_per_frame if fast_forward_enabled else normal_steps_per_frame
    for _ in range(steps_this_frame):
        # Update simulation time (12 hours per 15 seconds)
        simulation_hours += 12 / (15 * 60)  # 0.01333 hours per logic step at 60 FPS baseline

        # Spawn food at the configured simulated-hour interval.
        if simulation_hours - last_food_spawn >= food_spawn_interval:
            for _ in range(food_spawn_count):
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

        current_hour_mark = int(simulation_hours)
        if current_hour_mark > last_logged_hour:
            time_history.append(simulation_hours)
            prey_population_history.append(len(prey_list))
            predator_population_history.append(len(predator_list))
            food_population_history.append(len(food_list))
            last_logged_hour = current_hour_mark

        if len(prey_list) == 0 and len(predator_list) == 0:
            all_fish_dead = True
            running = False
            break

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
    time_text = font.render(f"Time: {hours:02d}:{minutes:02d}", True, (255, 255, 255))
    time_rect = time_text.get_rect(topright=(screen.get_width() - 10, 10))
    screen.blit(time_text, time_rect)

    button_color = (40, 170, 40) if fast_forward_enabled else (80, 80, 80)
    pygame.draw.rect(screen, button_color, button_rect, border_radius=8)
    button_label = "Fast Forward: ON (10x)" if fast_forward_enabled else "Fast Forward: OFF"
    button_text = button_font.render(button_label, True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)

    clock.tick(60)
    pygame.display.flip()
pygame.quit()
#Data Export logic
if args.csv_output:
    csv_output_path = Path(args.csv_output)
else:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_output_path = Path(f"simulation_stats_{timestamp}.csv")

with csv_output_path.open("w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["simulation_hours", "prey_population", "predator_population", "food_population"])
    for i in range(len(time_history)):
        writer.writerow(
            [
                f"{time_history[i]:.4f}",
                prey_population_history[i],
                predator_population_history[i],
                food_population_history[i],
            ]
        )
print(f"Saved simulation stats to: {csv_output_path}")

plt.figure(figsize=(10, 5))
plt.plot(time_history, prey_population_history, color="blue", label="Prey Population")
plt.plot(time_history, predator_population_history, color="red", label="Predator Population")
plt.plot(time_history, food_population_history, color="forestgreen", label="Food Population")
plt.title("Predator, Prey, and Food Population Over Time")
plt.xlabel("Simulation Time (hours)")
plt.ylabel("Population")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()



