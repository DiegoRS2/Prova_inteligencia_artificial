def solve_maze(maze, start, end):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Direções: direita, baixo, esquerda, cima

    def is_valid(x, y):
        return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] == 0

    def move(x, y, dir):
        return x + directions[dir][0], y + directions[dir][1]

    def manhattan_distance(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    x, y = start
    path = [(x, y)]
    last_x, last_y = x, y

    while (x, y) != end:
        min_dist = float('inf')
        next_x, next_y = x, y

        for dir in range(4):
            new_x, new_y = move(x, y, dir)
            if is_valid(new_x, new_y):
                dist = manhattan_distance(new_x, new_y, end[0], end[1])
                if dist < min_dist:
                    min_dist = dist
                    next_x, next_y = new_x, new_y

        if (next_x, next_y) == (x, y):
            # Se não houver movimentos válidos, retroceder
            if len(path) <= 1:
                # Não foi possível encontrar um caminho
                return None
            maze[x][y] = 2  # Marcar como visitado
            last_x, last_y = x, y
            x, y = path[-2]
            path.pop()
        else:
            maze[x][y] = 2  # Marcar como visitado
            last_x, last_y = x, y
            x, y = next_x, next_y
            path.append((x, y))

    return path

# Exemplo de uso
maze = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 1],
    [0, 1, 1, 1, 1]
]

start = (4, 0)
end = (2, 1)

path = solve_maze(maze, start, end)
if path:
    print("Caminho encontrado:")
    for step in path:
        print(step)
else:
    print("Não foi possível encontrar um caminho.")
