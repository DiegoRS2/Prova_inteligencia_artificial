import tkinter as tk
import heapq


MilliSecSpeed = 500


class Node:
    def __init__(self, puzzle: list[int], parent: 'Node' = None, move: str = ""):
        self.puzzle = puzzle
        self.parent = parent
        self.move = move
        self.cost = 0

    def __lt__(self, other):
        return self.cost < other.cost


def misplaced_tiles(puzzle: list[int], goal: list[int]):
    return sum(puzzle[i] != goal[i] for i in range(15))


def solve_puzzle(initial_state: list[int], goal_state: list[int]):
    open_set: list[Node] = []
    closed_set = set()

    initial_node = Node(initial_state)
    initial_node.cost = misplaced_tiles(initial_state, goal_state)

    heapq.heappush(open_set, initial_node)

    while open_set:
        current_node: Node = heapq.heappop(open_set)

        if current_node.puzzle == goal_state:
            path: list[Node] = []
            while current_node:
                path.append(current_node)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(tuple(current_node.puzzle))

        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in moves:
            x, y = (
                current_node.puzzle.index(0) // 4 + dx,
                current_node.puzzle.index(0) % 4 + dy,
            )

            if 0 <= x < 4 and 0 <= y < 4:
                new_puzzle = current_node.puzzle[:]
                new_puzzle[current_node.puzzle.index(0)], new_puzzle[x * 4 + y] = (
                    new_puzzle[x * 4 + y],
                    new_puzzle[current_node.puzzle.index(0)],
                )
                if tuple(new_puzzle) not in closed_set:
                    new_node = Node(
                        new_puzzle,
                        current_node,
                        move=f"Move {current_node.puzzle.index(0)} to ({x}, {y})",
                    )
                    new_node.cost = len(new_node.move) + misplaced_tiles(
                        new_puzzle, goal_state
                    )
                    heapq.heappush(open_set, new_node)

    return None


# Função para atualizar a interface gráfica
def update_puzzle(puzzle):
    for i in range(4):
        for j in range(4):
            value = puzzle[i * 4 + j]
            buttons[i][j].config(
                text=str(value) if value != 0 else "", state=tk.DISABLED
            )


# Função para atualizar a interface gráfica automaticamente
# ...

# Função para atualizar a interface gráfica automaticamente
# ...


# Função para atualizar a interface gráfica automaticamente
def auto_update_gui():
    if solution_path:
        current_node = solution_path.pop(0)
        label.config(text=f"Move: {current_node.move}")
        update_puzzle(current_node.puzzle)
        root.after(MilliSecSpeed, auto_update_gui)


# Configuração da interface gráfica
root = tk.Tk()
root.title("15 Puzzle Solver")

frame = tk.Frame(root)
frame.pack(pady=10)

buttons = [
    [
        tk.Button(
            frame,
            width=5,
            height=2,
            font=("Helvetica", 12),
            command=lambda i=i, j=j: move_tile(i, j),
        )
        for j in range(4)
    ]
    for i in range(4)
]

label = tk.Label(root, text="", font=("Helvetica", 14))
label.pack(pady=10)

# Usando o gerenciador de geometria grid para os botões dentro do frame
for i in range(4):
    for j in range(4):
        buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

# Defina a posição inicial do quebra-cabeça
initial_state = [12, 1, 2, 15, 11, 6, 5, 8, 7, 10, 9, 4, 0, 13, 14, 3]

# Defina o estado final do quebra-cabeça
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

# Resolva o quebra-cabeça
solution_path = solve_puzzle(initial_state, goal_state)


# Função para mover a peça no botão clicado
def move_tile(i, j):
    if solution_path:
        auto_update_gui()


# Função para iniciar a atualização automática
def start_auto_update():
    auto_update_gui()


# Adicionando um botão para iniciar a atualização automática
start_button = tk.Button(root, text="Start Auto Update", command=start_auto_update)
start_button.pack(pady=10)

# Atualize a interface gráfica com o estado inicial
update_puzzle(initial_state)

root.mainloop()
