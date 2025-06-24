# pathfinder.py
from collections import deque

def find_shortest_path_bfs(maze, start, goal, allowed_values):
    height = len(maze)
    width = len(maze[0])
    visited = [[False] * width for _ in range(height)]
    prev = [[None] * width for _ in range(height)]

    queue = deque()
    queue.append(start)
    visited[start[1]][start[0]] = True

    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            break
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if not visited[ny][nx] and maze[ny][nx] in allowed_values:
                    visited[ny][nx] = True
                    prev[ny][nx] = (x, y)
                    queue.append((nx, ny))

    path = []
    cur = goal
    while cur and cur != start:
        path.append(cur)
        cur = prev[cur[1]][cur[0]]
    if cur == start:
        path.append(start)
        path.reverse()
        return path
    return []
