def solve_maze(maze, start, end):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Direções: direita, baixo, esquerda, cima

    def is_valid(x, y):
        return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] == 0

    def move(x, y, dir):
        return x + directions[dir][0], y + directions[dir][1]

    x, y = start
    path = [(x, y)]
    last_x, last_y = x, y

    while (x, y) != end:
        found = False
        for dir in range(4):
            next_x, next_y = move(x, y, dir)
            if is_valid(next_x, next_y) and (next_x, next_y) != (last_x, last_y):
                maze[x][y] = 2  # Marcar como visitado
                last_x, last_y = x, y
                x, y = next_x, next_y
                path.append((x, y))
                found = True
                break

        if not found:
            # Se não houver movimentos válidos, retroceder
            if len(path) <= 1:
                # Não foi possível encontrar um caminho
                return None
            maze[x][y] = 2  # Marcar como visitado
            last_x, last_y = x, y
            x, y = path[-2]
            path.pop()

    return path

# Exemplo de uso
maze = [
    [1, 1, 1, 1, 1],
    [0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1]
]

start = (1, 0)
end = (3, 4)

path = solve_maze(maze, start, end)
if path:
    print("Caminho encontrado:")
    for step in path:
        print(step)
else:
    print("Não foi possível encontrar um caminho.")
