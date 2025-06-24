import pygame
import random
import math
from collections import deque

# ------------ 迷宮生成 + 增加連通性 ------------
def generate_maze(width, height):
    width = width if width % 2 == 1 else width + 1
    height = height if height % 2 == 1 else height + 1
    maze = [[1 for _ in range(width)] for _ in range(height)]


    def carve_passages(x, y):
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and maze[ny][nx] == 1:
                maze[ny][nx] = 0
                maze[y + dy // 2][x + dx // 2] = 0
                carve_passages(nx, ny)

    maze[1][1] = 0
    carve_passages(1, 1)
    maze[height - 2][width - 2] = 0
    return maze

def add_extra_connections(maze, chance=0.2):
    height = len(maze)
    width = len(maze[0])
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if maze[y][x] == 1 and ((x % 2 == 1 and y % 2 == 0) or (x % 2 == 0 and y % 2 == 1)):
                if random.random() < chance:
                    maze[y][x] = 0

# ------------ 小球移動模擬退火邏輯 ------------
def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def simulated_annealing_stepwise(maze, start, end, screen, draw_func):
    current_pos = start
    path = [current_pos]
    visited = set()

    T = 100.0
    Tmin = 0.1
    alpha = 0.98

    while current_pos != end:
        neighbors = []
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = current_pos[0] + dx, current_pos[1] + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0:
                neighbors.append((nx, ny))

        if not neighbors:
            break

        next_pos = random.choice(neighbors)
        e_current = manhattan_distance(current_pos, end)
        e_next = manhattan_distance(next_pos, end)
        delta = e_next - e_current

        accepted = False
        if delta < 0 or random.random() < math.exp(-delta / T):
            current_pos = next_pos
            path.append(current_pos)
            accepted = True

        draw_func(screen, maze, path, current_pos, T, accepted)
        pygame.display.flip()
        pygame.time.wait(40)

        T *= alpha
        if T < Tmin:
            T = 100.0
            current_pos = start
            path = [current_pos]

# ------------ Pygame 視覺化 ------------
CELL_SIZE = 15
MAZE_WIDTH = 41
MAZE_HEIGHT = 41
WINDOW_WIDTH = MAZE_WIDTH * CELL_SIZE
WINDOW_HEIGHT = MAZE_HEIGHT * CELL_SIZE + 40

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (50,255,50)
RED = (255,50,50)
BLUE = (50,50,255)
YELLOW = (255,255,0)
GRAY = (180, 180, 255)


def get_background_color(temp):
    scale = max(0, min(255, int(255 * (temp / 100))))
    return (255 - scale, 255 - scale, 255)

def draw_maze(screen, maze, temp):
    bg_color = get_background_color(temp)
    screen.fill(bg_color)
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            color = BLACK if maze[y][x] == 1 else WHITE
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE))

def draw_stepwise(screen, maze, path, current_pos, temp, accepted):
    draw_maze(screen, maze, temp)

    for (x, y) in path:
        pygame.draw.rect(screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE))

    x, y = current_pos
    pygame.draw.rect(screen, BLUE if accepted else RED, (x * CELL_SIZE, y * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(screen, GREEN, (1 * CELL_SIZE, 1 * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, YELLOW, ((MAZE_WIDTH - 2) * CELL_SIZE, (MAZE_HEIGHT - 2) * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE))

    font = pygame.font.SysFont(None, 24)
    temp_text = font.render(f"T = {temp:.2f}  |  Steps = {len(path)}", True, (0, 0, 0))
    screen.blit(temp_text, (10, 5))

# ------------ 主程式 ------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Stepwise Simulated Annealing Maze")

    maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
    add_extra_connections(maze, chance=0.2)

    start = (1,1)
    end = (MAZE_WIDTH - 2, MAZE_HEIGHT - 2)

    simulated_annealing_stepwise(maze, start, end, screen, draw_stepwise)

if __name__ == "__main__":
    main()
