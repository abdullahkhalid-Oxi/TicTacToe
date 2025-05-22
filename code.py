# tic_tac_toe.py

import math
import time

# Constants
HUMAN = 'X'
AI = 'O'
EMPTY = ' '

# Initialize board
board = [[EMPTY for _ in range(3)] for _ in range(3)]

# Utility functions
def print_board():
    for row in board:
        print('|'.join(row))
        print('-' * 5)

def is_moves_left():
    return any(EMPTY in row for row in board)

def evaluate():
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return 1 if board[i][0] == AI else -1
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return 1 if board[0][i] == AI else -1

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return 1 if board[0][0] == AI else -1
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return 1 if board[0][2] == AI else -1

    return 0

def minimax(depth, is_max):
    score = evaluate()
    if score != 0 or not is_moves_left():
        return score

    if is_max:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    best = max(best, minimax(depth + 1, not is_max))
                    board[i][j] = EMPTY
        return best
    else:
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = HUMAN
                    best = min(best, minimax(depth + 1, not is_max))
                    board[i][j] = EMPTY
        return best

def minimax_ab(depth, is_max, alpha, beta):
    score = evaluate()
    if score != 0 or not is_moves_left():
        return score

    if is_max:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    val = minimax_ab(depth + 1, False, alpha, beta)
                    best = max(best, val)
                    alpha = max(alpha, best)
                    board[i][j] = EMPTY
                    if beta <= alpha:
                        break
        return best
    else:
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = HUMAN
                    val = minimax_ab(depth + 1, True, alpha, beta)
                    best = min(best, val)
                    beta = min(beta, best)
                    board[i][j] = EMPTY
                    if beta <= alpha:
                        break
        return best

def best_move(use_alpha_beta=False):
    best_val = -math.inf
    move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                move_val = minimax_ab(0, False, -math.inf, math.inf) if use_alpha_beta else minimax(0, False)
                board[i][j] = EMPTY
                if move_val > best_val:
                    move = (i, j)
                    best_val = move_val

    return move

def play_game(use_alpha_beta=False):
    print("Welcome to Tic-Tac-Toe!")
    print_board()
    
    while True:
        # Human move
        row = int(input("Enter row (0-2): "))
        col = int(input("Enter column (0-2): "))
        if board[row][col] != EMPTY:
            print("Invalid move. Try again.")
            continue
        board[row][col] = HUMAN
        print_board()
        if evaluate() == -1:
            print("You win!")
            break
        if not is_moves_left():
            print("It's a draw!")
            break

        # AI move
        print("AI is thinking...")
        start = time.time()
        i, j = best_move(use_alpha_beta)
        end = time.time()
        board[i][j] = AI
        print_board()
        print(f"AI moved in {(end - start):.4f} seconds")
        if evaluate() == 1:
            print("AI wins!")
            break
        if not is_moves_left():
            print("It's a draw!")
            break

if __name__ == '__main__':
    choice = input("Use Alpha-Beta Pruning? (y/n): ").lower()
    play_game(use_alpha_beta=(choice == 'y'))
