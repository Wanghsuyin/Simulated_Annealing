# main.py
import pygame
from maze_generator import generate_maze, apply_temperature_levels
from pathfinder import find_shortest_path_bfs

# Colors
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
WHITE = (255, 255, 255)
LIGHT_RED = (255, 182, 193)
RED = (255, 69, 0)
GRAY = (200, 200, 200)
PURPLE = (128, 0, 128)

# Maze and cell settings
CELL_SIZE = 12
MAZE_WIDTH = 41
MAZE_HEIGHT = 41

def draw_maze(screen, maze):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1:
                color = BLACK
            elif cell == 0:
                color = LIGHT_BLUE
            elif cell == 30:
                color = WHITE
            elif cell == 100:
                color = LIGHT_RED
            elif cell == 300:
                color = RED
            else:
                color = GRAY

            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)

def draw_path_ball(screen, position):
    x, y = position
    cx = x * CELL_SIZE + CELL_SIZE // 2
    cy = y * CELL_SIZE + CELL_SIZE // 2
    radius = CELL_SIZE // 3
    pygame.draw.circle(screen, PURPLE, (cx, cy), radius)

def main():
    pygame.init()
    screen_width = MAZE_WIDTH * CELL_SIZE
    screen_height = MAZE_HEIGHT * CELL_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Simulated Annealing Maze - Animated Path")

    font = pygame.font.SysFont(None, 24)

    # 🌀 Switch between 'dfs' and 'prim'
    generation_method = "dfs"
    maze = generate_maze(generation_method, MAZE_WIDTH, MAZE_HEIGHT, seed=42)

    temperature_levels = [10, 30, 100, 300]
    current_temperature_index = 0
    print(f"[INIT] Initial temperature: {temperature_levels[current_temperature_index]}°C")

    full_path = []
    path_progress = 0
    is_animating = False
    path_length = 0

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)
        draw_maze(screen, maze)

        for i in range(path_progress):
            draw_path_ball(screen, full_path[i])
        if is_animating and path_progress < len(full_path):
            draw_path_ball(screen, full_path[path_progress])
            path_progress += 1
        elif is_animating and path_progress >= len(full_path):
            is_animating = False

        # UI display
        temp_text = f"Temperature: {temperature_levels[current_temperature_index]}°C" \
            if current_temperature_index < len(temperature_levels) else "Max Temperature Reached"
        step_text = f"Steps: {min(path_progress, len(full_path))}"
        length_text = f"Path Length: {path_length}"
        algo_text = f"Maze: {generation_method.upper()}"

        screen.blit(font.render(temp_text, True, (255, 255, 0)), (10, 10))
        screen.blit(font.render(step_text, True, (0, 255, 255)), (10, 30))
        screen.blit(font.render(length_text, True, (200, 200, 255)), (10, 50))
        screen.blit(font.render(algo_text, True, (180, 180, 180)), (10, 70))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_RIGHT) and not is_animating:
                    current_temperature_index += 1
                    if current_temperature_index < len(temperature_levels):
                        temperature = temperature_levels[current_temperature_index]
                        print(f"[INFO] Raised temperature to {temperature}°C")
                        maze = apply_temperature_levels(maze, temperature)

                        allowed = [0] + temperature_levels[1:current_temperature_index + 1]
                        full_path = find_shortest_path_bfs(
                            maze, (1, 1), (MAZE_WIDTH - 2, MAZE_HEIGHT - 2), allowed)
                        path_length = len(full_path)
                        print(f"[INFO] Path length: {path_length}")

                        path_progress = 0
                        is_animating = True
                    else:
                        print("[INFO] Maximum temperature reached")

        pygame.display.flip()
        clock.tick(15)

    pygame.quit()

if __name__ == "__main__":
    main()
