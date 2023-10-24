import random

def display_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 9)
    print("\n")

def check_winner(board, player):
    for row in board:
        if all([cell == player for cell in row]):
            return True

    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True

    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True

    return False

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def minimax(board, depth, maximizing_player):
    if check_winner(board, 'O'):
        return 1
    if check_winner(board, 'X'):
        return -1
    if is_board_full(board):
        return 0

    if maximizing_player:
        max_eval = -float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    eval = minimax(board, depth - 1, False)
                    board[row][col] = ' '
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    eval = minimax(board, depth - 1, True)
                    board[row][col] = ' '
                    min_eval = min(min_eval, eval)
        return min_eval

def make_best_move(board, player):
    best_move = None
    best_eval = -float('inf') if player == 'O' else float('inf')
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = player
                eval = minimax(board, 9, player == 'O')
                board[row][col] = ' '
                if player == 'O':
                    if eval > best_eval:
                        best_eval = eval
                        best_move = (row, col)
                else:
                    if eval < best_eval:
                        best_eval = eval
                        best_move = (row, col)
    return best_move

def play_game():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'O'
    while True:
        display_board(board)
        if is_board_full(board):
            print("empate")
            break
        if check_winner(board, 'O'):
            print("Jogador 'O' (bolinha) venceu!")
            break
        elif check_winner(board, 'X'):
            print("Jogador 'X' venceu!")
            break

        if current_player == 'O':
            row, col = make_best_move(board, current_player)
        else:
            row, col = make_best_move(board, current_player)

        board[row][col] = current_player
        current_player = 'X' if current_player == 'O' else 'O'

play_game()
