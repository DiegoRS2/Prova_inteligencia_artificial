from typing import List, Tuple

class Maze:

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.maze = [[0 for _ in range(width)] for _ in range(height)]

    def add_wall(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        self.maze[start[0]][start[1]] = 1
        self.maze[end[0]][end[1]] = 1

    def get_neighbors(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:

        neighbors = []
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            new_x = position[0] + dx
            new_y = position[1] + dy
            if 0 <= new_x < self.width and 0 <= new_y < self.height and self.maze[new_x][new_y] == 0:
                neighbors.append((new_x, new_y))
        return neighbors

    def get_distance(self, start: Tuple[int, int], end: Tuple[int, int]) -> int:
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

def maze_search(maze: Maze, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    open_list = []
    closed_list = set()

    path = []
    open_list.append((start, 0))

    while open_list:
        current_position, current_cost = open_list.pop(0)

        path.append(current_position)

        print(f"Caminho atual: {path} \n")

        if current_position == goal:
            return reconstruct_path(open_list, current_position)

        closed_list.add(current_position)

        for neighbor in maze.get_neighbors(current_position):
            neighbor_cost = current_cost + maze.get_distance(current_position, neighbor)

            if neighbor not in open_list and neighbor not in closed_list:
                open_list.append((neighbor, neighbor_cost))

    return None




def reconstruct_path(open_list, current_position):
    path = [current_position]
    while current_position in open_list:
        current_position, _ = open_list[current_position]
        path.append(current_position)
    return path

if __name__ == "__main__":
    maze = Maze(5, 5)

    maze.add_wall((1, 0), (2, 0))
    maze.add_wall((2, 0), (2, 1))
    maze.add_wall((2, 1), (2, 2))
    maze.add_wall((3, 2), (3, 3))

    start = (0, 0)
    end = (4, 4)

    path = maze_search(maze, start, end)
    if path:
        print("Caminho encontrado:")
        for step in path:
            print(step)
    else:
        print("Não foi possível encontrar um caminho.")


