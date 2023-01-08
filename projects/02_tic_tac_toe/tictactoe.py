"""
Tic Tac Toe Player
"""

import math
import copy
X = "X"
O = "O"
# possible move in the board
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    X_count = 0
    O_count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                continue
            elif board[i][j] == X:
                X_count += 1
            else:
                O_count += 1

    if X_count <= O_count:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    res = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                res.add((i, j))
    return res

def range_check(action, row=3, col=3):
    if action[0] < 0 or action[0] > row:
        return False
    if action[1] < 0 or action[1] > col:
        return False
    return True

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.

    Importantly, the original board should be left unmodified: 
    since Minimax will ultimately require considering 
    many different board states during its computation.
    """
    if not range_check(action, len(board), len(board)):
        raise ValueError(f"result: board range error for {action}.")

    next_board = copy.deepcopy(board)

    if board[action[0]][action[1]] is EMPTY:
        next_board[action[0]][action[1]] = player(board)
    else:
        raise ValueError(f"result: board in {action} is not empty.")

    return next_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    You may assume that there will be at most one winner
    Returns None, if there is no winner(tie or processing)
    """
    # check row
    posi_winner = None
    winner_flag = False
    for i in range(len(board)):
        if board[i][0] is None:
            continue
        else:
            posi_winner = board[i][0]
            winner_flag = True
        for j in range(len(board[i])):
            if board[i][j] is None or board[i][j] != posi_winner:
                winner_flag = False
                break
        if winner_flag:
            return posi_winner

    # check column
    for j in range(len(board[0])):
        if board[0][j] is None:
            continue
        else:
            posi_winner = board[0][j]
            winner_flag = True
        for i in range(len(board)):
            if board[i][j] is None or board[i][j] != posi_winner:
                winner_flag = False;
                break
        if winner_flag:
            return posi_winner

    # check diag
    for i in range(len(board)):
        if board[0][0] is None:
            break
        else:
            posi_winner = board[0][0]
            winner_flag = True
        for j in range(len(board)):
            if board[j][j] is None or board[j][j] != posi_winner:
                winner_flag = False
                break
        if winner_flag:
            return posi_winner

    for i in range(len(board)):
        if board[0][len(board)-1] is None:
            break
        else:
            posi_winner = board[0][len(board)-1]
            winner_flag = True
        for j in range(len(board)):
            if board[j][len(board)-1-j] is None or board[j][len(board)-1-j] != posi_winner:
                winner_flag = False
                break
        if winner_flag:
            return posi_winner

    return None

def check_full(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] is EMPTY:
                return False
    return True

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if check_full(board) or winner(board):
        return True
    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    utility will only be called on a board if terminal(board) is True.
    """
    winner_player = winner(board)
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0

def alpha_bate_pruning(val, opti_vals, curr_player, bound):
    # second level: opti_vals, curr_level
    # val is third level
    if curr_player == X:    # first level is O
        for i in range(bound):
            # curr second_level's node (from top --(action)--> second)
            # is >= val for X chooes max.
            # however, the top is O, will only choose min, so
            # the curr second_level's node will not be considered
            # for curr second_level's node > other second_level's node
            if val > opti_vals[i]:
                return True
    if curr_player == O:    # first levle is X
        for i in range(bound):
            if val < opti_vals[i]:
                return True
    return False

def dfs_minimax(board, opti_vals_par, bound):

    if terminal(board):
        return utility(board)

    posi_actions = actions(board)
    curr_player = player(board)
    # X need to max curr_val, O need to min
    # safe for -2 and 2

    opti_val = -2 if curr_player == X else 2
    opti_vals = [-2 for i in range(len(posi_actions))] \
            if curr_player == X else [2 for i in range(len(posi_actions))]

    for idx, action in enumerate(posi_actions):
        new_board = result(board, action)
        tmp_val = dfs_minimax(new_board, opti_vals, idx)
        if curr_player == X and opti_vals[idx] < tmp_val:
            opti_vals[idx] = tmp_val
            if (alpha_bate_pruning(opti_vals[idx], opti_vals_par, curr_player, bound)):
                break
        if curr_player == O and opti_vals[idx] > tmp_val:
            opti_vals[idx] = tmp_val
            if (alpha_bate_pruning(opti_vals[idx], opti_vals_par, curr_player, bound)):
                break


    for val in opti_vals:
        if curr_player == X and opti_val < val:
            opti_val = val
        if curr_player == O and opti_val > val:
            opti_val = val
    # return second_level's node val
    return opti_val

def minimax(board):
    """
    Returns the optimal action (i, j) for the current player on the board.
    If multiple moves are equally optimal, any of those moves is acceptable.
    If the board is a terminal board, the minimax function should return None.
    """

    posi_actions = actions(board)
    curr_player = player(board)
    optimal_action = None
    optimal_actions = [None for i in range(len(posi_actions))]
    # X need to max curr_val, O need to min
    # safe for -2 and 2
    opti_val = -2 if curr_player == X else 2
    opti_vals = [-2 for i in range(len(posi_actions))] \
            if curr_player == X else [2 for i in range(len(posi_actions))]

    for idx, action in enumerate(posi_actions):
        new_board = result(board, action)
        tmp_val = dfs_minimax(new_board, opti_vals, idx)
        if curr_player == X and opti_vals[idx] < tmp_val:
            opti_vals[idx] = tmp_val
            optimal_actions[idx] = action
        if curr_player == O and opti_vals[idx] > tmp_val:
            opti_vals[idx] = tmp_val
            optimal_actions[idx] = action
    
    for idx, val in enumerate(opti_vals):
        if curr_player == X and opti_val < val:
            opti_val = val
            optimal_action = optimal_actions[idx]
        if curr_player == O and opti_val > val:
            opti_val = val
            optimal_action = optimal_actions[idx]
    return optimal_action