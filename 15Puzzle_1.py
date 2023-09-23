import heapq

class Node:
    def __init__(self, puzzle, parent=None, move=""):
        self.puzzle = puzzle
        self.parent = parent
        self.move = move
        self.cost = 0

    def __lt__(self, other):
        return self.cost < other.cost

def misplaced_tiles(puzzle, goal):
    return sum(puzzle[i] != goal[i] for i in range(15))

def solve_puzzle(initial_state, goal_state):
    open_set = []
    closed_set = set()

    initial_node = Node(initial_state)
    initial_node.cost = misplaced_tiles(initial_state, goal_state)

    heapq.heappush(open_set, initial_node)

    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node.puzzle == goal_state:
            path = []
            while current_node:
                path.append(current_node.move)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(tuple(current_node.puzzle))

        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in moves:
            x, y = current_node.puzzle.index(0) // 4 + dx, current_node.puzzle.index(0) % 4 + dy

            if 0 <= x < 4 and 0 <= y < 4:
                new_puzzle = current_node.puzzle[:]
                new_puzzle[current_node.puzzle.index(0)], new_puzzle[x * 4 + y] = new_puzzle[x * 4 + y], new_puzzle[current_node.puzzle.index(0)]
                if tuple(new_puzzle) not in closed_set:
                    new_node = Node(new_puzzle, current_node, move=f"Move {current_node.puzzle.index(0)} to ({x}, {y})")
                    new_node.cost = len(new_node.move) + misplaced_tiles(new_puzzle, goal_state)
                    heapq.heappush(open_set, new_node)

    return None

initial_state = [12, 1, 2, 15, 11, 6, 5, 8, 7, 10, 9, 4, 0, 13, 14, 3]
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

solution = solve_puzzle(initial_state, goal_state)
if solution:
    for i, move in enumerate(solution):
        print(f"Step {i + 1}: {move}")
else:
    print("Não há solução para o quebra-cabeça fornecido.")
