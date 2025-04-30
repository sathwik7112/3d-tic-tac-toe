# backend/game_logic.py

import math

# ─────────────────────────────────────────────────────────────
# Constants & Winning‐Line Definitions
# ─────────────────────────────────────────────────────────────
EMPTY = '.'
HUMAN = 'X'
AI    = 'O'

# Precompute the 76 winning lines in a 4×4×4 cube
LINES = []

# rows, cols, and diagonals within each level
for z in range(4):
    for y in range(4):
        LINES.append([(z, y, x) for x in range(4)])
    for x in range(4):
        LINES.append([(z, y, x) for y in range(4)])
    LINES.append([(z, i, i)     for i in range(4)])
    LINES.append([(z, i, 3 - i) for i in range(4)])

# vertical pillars
for y in range(4):
    for x in range(4):
        LINES.append([(z, y, x) for z in range(4)])

# diagonals in vertical planes
for x in range(4):
    LINES.append([(i, i, x)     for i in range(4)])
    LINES.append([(i, 3 - i, x) for i in range(4)])
for y in range(4):
    LINES.append([(i, y, i)     for i in range(4)])
    LINES.append([(i, y, 3 - i) for i in range(4)])

# four space diagonals
LINES += [
    [(i, i, i)       for i in range(4)],
    [(i, i, 3 - i)   for i in range(4)],
    [(i, 3 - i, i)   for i in range(4)],
    [(i, 3 - i, 3 - i) for i in range(4)],
]

# ─────────────────────────────────────────────────────────────
# Board Creation & Game‐Over Check
# ─────────────────────────────────────────────────────────────
def make_empty_board():
    """Return a fresh 4×4×4 board filled with EMPTY."""
    return [[[EMPTY]*4 for _ in range(4)] for __ in range(4)]

def check_game_over(board):
    """
    Return HUMAN if X has a winning line,
           AI    if O has a winning line,
           'tie' if board full with no winner,
           None  otherwise.
    """
    # check wins
    for line in LINES:
        marks = [board[z][y][x] for (z, y, x) in line]
        if all(m == HUMAN for m in marks):
            return HUMAN
        if all(m == AI for m in marks):
            return AI
    # check tie
    if all(cell != EMPTY for lvl in board for row in lvl for cell in row):
        return 'tie'
    return None

# ─────────────────────────────────────────────────────────────
# Minimax + α–β Pruning AI
# ─────────────────────────────────────────────────────────────
def evaluate(board):
    """Heuristic: +10^n for n-in-line of O (AI), -10^n for X (HUMAN)."""
    score = 0
    for line in LINES:
        ai_count = human_count = 0
        for z, y, x in line:
            if board[z][y][x] == AI:
                ai_count += 1
            elif board[z][y][x] == HUMAN:
                human_count += 1
        if ai_count and not human_count:
            score += 10 ** ai_count
        elif human_count and not ai_count:
            score -= 10 ** human_count
    return score

def get_moves(board):
    """Return all empty (z,y,x) triples."""
    return [
        (z, y, x)
        for z in range(4)
        for y in range(4)
        for x in range(4)
        if board[z][y][x] == EMPTY
    ]

def alpha_beta(board, depth, alpha, beta, maximizing):
    """
    Standard α–β.  maximizing=True for AI's turn, False for HUMAN's.
    Returns (score, best_move).
    """
    # terminal checks
    result = check_game_over(board)
    if result == AI:    return math.inf, None
    if result == HUMAN: return -math.inf, None
    if depth == 0:
        return evaluate(board), None

    best_move = None
    if maximizing:
        max_eval = -math.inf
        for move in get_moves(board):
            z, y, x = move
            board[z][y][x] = AI
            val, _ = alpha_beta(board, depth-1, alpha, beta, False)
            board[z][y][x] = EMPTY
            if val > max_eval:
                max_eval, best_move = val, move
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in get_moves(board):
            z, y, x = move
            board[z][y][x] = HUMAN
            val, _ = alpha_beta(board, depth-1, alpha, beta, True)
            board[z][y][x] = EMPTY
            if val < min_eval:
                min_eval, best_move = val, move
            beta = min(beta, val)
            if beta <= alpha:
                break
        return min_eval, best_move
