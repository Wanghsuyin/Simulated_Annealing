# maze_generator.py
import random

WALL = 1
PATH = 0

def generate_maze_with_prim(width, height, seed=None):
    if seed is not None:
        random.seed(seed)

    width = width if width % 2 == 1 else width - 1
    height = height if height % 2 == 1 else height - 1
    maze = [[WALL for _ in range(width)] for _ in range(height)]

    start_x = random.randrange(1, width, 2)
    start_y = random.randrange(1, height, 2)
    maze[start_y][start_x] = PATH

    frontier = []

    def add_frontiers(x, y):
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nx, ny = x + dx, y + dy
            if 0 < nx < width and 0 < ny < height and maze[ny][nx] == WALL:
                frontier.append((nx, ny, x, y))

    add_frontiers(start_x, start_y)

    while frontier:
        idx = random.randint(0, len(frontier) - 1)
        x, y, from_x, from_y = frontier.pop(idx)

        if maze[y][x] == WALL:
            maze[y][x] = PATH
            maze[(y + from_y) // 2][(x + from_x) // 2] = PATH
            add_frontiers(x, y)

    return maze


def generate_maze_with_dfs(width, height, seed=None):
    if seed is not None:
        random.seed(seed)

    width = width if width % 2 == 1 else width - 1
    height = height if height % 2 == 1 else height - 1
    maze = [[WALL for _ in range(width)] for _ in range(height)]

    def carve(x, y):
        dirs = [(2,0), (-2,0), (0,2), (0,-2)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and maze[ny][nx] == WALL:
                maze[ny][nx] = PATH
                maze[y + dy//2][x + dx//2] = PATH
                carve(nx, ny)

    start_x = random.randrange(1, width, 2)
    start_y = random.randrange(1, height, 2)
    maze[start_y][start_x] = PATH
    carve(start_x, start_y)

    return maze


def generate_maze(method, width, height, seed=None):
    if method == "prim":
        return generate_maze_with_prim(width, height, seed)
    elif method == "dfs":
        return generate_maze_with_dfs(width, height, seed)
    else:
        raise ValueError(f"Unknown maze generation method: {method}")


def apply_temperature_levels(maze, temperature):
    height = len(maze)
    width = len(maze[0])

    if temperature == 30:
        ratio = 0.04
        tag = 30
    elif temperature == 100:
        ratio = 0.10
        tag = 100
    elif temperature == 300:
        ratio = 0.20
        tag = 300
    else:
        print(f"[WARN] Unsupported temperature: {temperature}")
        return maze

    candidates = [(x, y) for y in range(1, height - 1)
                  for x in range(1, width - 1) if maze[y][x] == WALL]

    if not candidates:
        print("[WARN] No wall tiles available to open")
        return maze

    num_to_open = int(len(candidates) * ratio)
    to_open = random.sample(candidates, num_to_open)

    for x, y in to_open:
        maze[y][x] = tag

    print(f"[INFO] Temperature {temperature}°C: Opened {num_to_open} walls (marked as {tag})")
    return maze
