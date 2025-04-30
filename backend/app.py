import os
import time
import math
import concurrent.futures
from flask import Flask, render_template, request, jsonify

# ─────────────────────────────────────────────────────────────
# Constants & Winning Lines
# ─────────────────────────────────────────────────────────────
EMPTY = '.'
HUMAN = 'X'
AI    = 'O'

# Precompute all 76 winning lines in the 4×4×4 cube
LINES = []
for z in range(4):
    for y in range(4):
        LINES.append([(z, y, x) for x in range(4)])
    for x in range(4):
        LINES.append([(z, y, x) for y in range(4)])
    LINES.append([(z, i, i)     for i in range(4)])
    LINES.append([(z, i, 3 - i) for i in range(4)])
for y in range(4):
    for x in range(4):
        LINES.append([(z, y, x) for z in range(4)])
for x in range(4):
    LINES.append([(i, i, x)     for i in range(4)])
    LINES.append([(i, 3 - i, x) for i in range(4)])
for y in range(4):
    LINES.append([(i, y, i)     for i in range(4)])
    LINES.append([(i, y, 3 - i) for i in range(4)])
LINES += [
    [(i, i, i)       for i in range(4)],
    [(i, i, 3 - i)   for i in range(4)],
    [(i, 3 - i, i)   for i in range(4)],
    [(i, 3 - i, 3 - i) for i in range(4)],
]

# ─────────────────────────────────────────────────────────────
# Transposition Table & Move Memory
# ─────────────────────────────────────────────────────────────
trans_table = {}
prev_best_moves = {}

def board_to_key(board):
    return tuple(tuple(tuple(row) for row in lvl) for lvl in board)

# ─────────────────────────────────────────────────────────────
# Game Logic
# ─────────────────────────────────────────────────────────────
def make_empty_board():
    return [[[EMPTY]*4 for _ in range(4)] for __ in range(4)]

def check_game_over(board):
    """Return HUMAN/AI if someone won, 'tie' if full with no winner, else None."""
    for line in LINES:
        marks = [board[z][y][x] for z, y, x in line]
        if all(m == HUMAN for m in marks): return HUMAN
        if all(m == AI    for m in marks): return AI
    if all(cell != EMPTY for lvl in board for row in lvl for cell in row):
        return 'tie'
    return None

def evaluate(board):
    """+10^n for n-in-line of AI-only, –10^n for HUMAN-only."""
    score = 0
    for line in LINES:
        ai_cnt = human_cnt = 0
        for z, y, x in line:
            if board[z][y][x] == AI:    ai_cnt += 1
            elif board[z][y][x] == HUMAN: human_cnt += 1
        if ai_cnt and not human_cnt:
            score += 10 ** ai_cnt
        elif human_cnt and not ai_cnt:
            score -= 10 ** human_cnt
    return score

def get_moves(board):
    """All empties; after 4 marks, only those adjacent to an occupied cell."""
    empties = [(z,y,x)
               for z in range(4)
               for y in range(4)
               for x in range(4)
               if board[z][y][x] == EMPTY]
    marks = sum(1 for lvl in board for row in lvl for c in row if c != EMPTY)
    if marks < 4:
        return empties
    neighs = set()
    for z in range(4):
        for y in range(4):
            for x in range(4):
                if board[z][y][x] != EMPTY:
                    for dz in (-1,0,1):
                        for dy in (-1,0,1):
                            for dx in (-1,0,1):
                                nz,ny,nx = z+dz, y+dy, x+dx
                                if 0 <= nz < 4 and 0 <= ny < 4 and 0 <= nx < 4:
                                    neighs.add((nz,ny,nx))
    moves = [m for m in empties if m in neighs]
    return moves or empties

def get_ordered_moves(board, maximizing):
    """Get and score potential moves for better alpha-beta pruning."""
    raw = get_moves(board)
    scored = []
    for mv in raw:
        z, y, x = mv
        board[z][y][x] = AI if maximizing else HUMAN
        sc = evaluate(board)
        board[z][y][x] = EMPTY
        scored.append((sc, mv))
    # Sort moves by score (higher first if maximizing, lower first if minimizing)
    scored.sort(key=lambda t: t[0], reverse=maximizing)
    return [mv for _, mv in scored]

def check_immediate_win(board, player):
    """Check if player can win in one move and return that move."""
    for mv in get_moves(board):
        z, y, x = mv
        board[z][y][x] = player
        winner = check_game_over(board)
        board[z][y][x] = EMPTY
        if winner == player:
            return mv
    return None

def alpha_beta(board, depth, alpha, beta, maximizing,
               start_time=None, time_limit=None):
    # 1) time cutoff
    if time_limit and (time.perf_counter() - start_time) > time_limit:
        return evaluate(board), None

    # 2) terminal checks
    result = check_game_over(board)
    if result == AI:    return math.inf, None
    if result == HUMAN: return -math.inf, None
    if result == 'tie': return 0, None
    if depth == 0:
        val = evaluate(board)
        return val, None

    # 3) transposition lookup
    key = (board_to_key(board), depth, maximizing)
    if key in trans_table:
        return trans_table[key]

    # 4) Check for immediate wins (optimization)
    if maximizing:
        win_move = check_immediate_win(board, AI)
        if win_move:
            trans_table[key] = (math.inf, win_move)
            return math.inf, win_move
    else:
        win_move = check_immediate_win(board, HUMAN)
        if win_move:
            trans_table[key] = (-math.inf, win_move)
            return -math.inf, win_move

    # 5) generate & order moves
    moves = get_ordered_moves(board, maximizing)

    # 6) recurse
    best_move = None
    if maximizing:
        best_val = -math.inf
        for mv in moves:
            z, y, x = mv
            board[z][y][x] = AI
            val, _ = alpha_beta(board, depth-1, alpha, beta,
                               False, start_time, time_limit)
            board[z][y][x] = EMPTY
            if val > best_val:
                best_val, best_move = val, mv
            alpha = max(alpha, val)
            if beta <= alpha or best_val == math.inf:  # Early cutoff
                break
    else:
        best_val = math.inf
        for mv in moves:
            z, y, x = mv
            board[z][y][x] = HUMAN
            val, _ = alpha_beta(board, depth-1, alpha, beta,
                               True, start_time, time_limit)
            board[z][y][x] = EMPTY
            if val < best_val:
                best_val, best_move = val, mv
            beta = min(beta, val)
            if beta <= alpha or best_val == -math.inf:  # Early cutoff
                break

    trans_table[key] = (best_val, best_move)
    return best_val, best_move

def run_alpha_beta_with_time(board, depth, start_time, time_limit):
    """Run alpha-beta with a time constraint and return results."""
    try:
        if (time.perf_counter() - start_time) > time_limit:
            return None, None, True  # timeout
        
        score, move = alpha_beta(
            board, depth,
            -math.inf, math.inf,
            True,
            start_time=start_time,
            time_limit=time_limit
        )
        
        timeout = (time.perf_counter() - start_time) > time_limit
        return score, move, timeout
    except Exception as e:
        print(f"Error at depth {depth}: {e}")
        return None, None, True

# ─────────────────────────────────────────────────────────────
# Flask App & Routes
# ─────────────────────────────────────────────────────────────
basedir       = os.path.abspath(os.path.dirname(__file__))
templates_dir = os.path.abspath(os.path.join(basedir, '..', 'templates'))
static_dir    = os.path.abspath(os.path.join(basedir, '..', 'static'))
app = Flask(__name__,
            template_folder=templates_dir,
            static_folder=static_dir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_status', methods=['POST'])
def check_status():
    data = request.get_json()
    board = data['board']
    res = check_game_over(board)
    return jsonify({
        'winner': res if res in (HUMAN, AI) else None,
        'draw':   (res == 'tie')
    })

@app.route('/ai_move', methods=['POST'])
def ai_move():
    global prev_best_moves
    print("⚙️ /ai_move called")
    data = request.get_json()
    board = data['board']
    max_depth = data['depth']
    print(f"    payload depth={max_depth}")

    best_move = None
    best_score = None
    last_completed_depth = 0
    t0 = time.perf_counter()
    time_limit = 5.0  # 5-second cutoff
    
    # Check if we already have a good move from previous searches
    game_key = board_to_key(board)
    if game_key in prev_best_moves:
        cached_move = prev_best_moves[game_key]
        z, y, x = cached_move
        if board[z][y][x] == EMPTY:
            best_move = cached_move
            print(f"[AI] Using cached move {best_move}")
    
    # Check for immediate winning move
    win_move = check_immediate_win(board, AI)
    if win_move:
        best_move = win_move
        best_score = math.inf
        print(f"[AI] Found immediate winning move {best_move}")
    # Check for immediate defensive move
    elif not best_move:
        block_move = check_immediate_win(board, HUMAN)
        if block_move:
            best_move = block_move
            print(f"[AI] Found blocking move {best_move}")
    
    # If no immediate move found, run iterative deepening search
    if not best_move or best_score != math.inf:  # Skip search if we have a winning move
        # Use all even depths for iterative deepening
        depths = list(range(2, max_depth + 1, 2))
        
        for depth in depths:
            trans_table.clear()  # Clear table for each new depth
            score, move, timeout = run_alpha_beta_with_time(board, depth, t0, time_limit)
            
            if timeout:
                print(f"[AI] Time limit reached during depth={depth}")
                break
                
            if move is not None:
                best_move, best_score = move, score
                last_completed_depth = depth
                prev_best_moves[game_key] = best_move  # Store best move
                print(f"[AI] completed depth={depth}, move={best_move}, score={best_score}")
                
                # If we found a winning move, no need to search deeper
                if score == math.inf:
                    print(f"[AI] Found winning move at depth {depth}")
                    break
    
    # apply best move
    if best_move:
        z, y, x = best_move
        board[z][y][x] = AI

    elapsed = time.perf_counter() - t0
    print(f"[AI] final depth={last_completed_depth}, took {elapsed:.3f}s, move={best_move}, score={best_score}")

    res = check_game_over(board)
    draw = (res == 'tie')
    return jsonify({
        'board': board,
        'move': best_move,
        'winner': res if res in (HUMAN, AI) else None,
        'draw': draw,
        'depth_reached': last_completed_depth,
        'time_taken': elapsed
    })

if __name__ == '__main__':
    app.run(debug=True)