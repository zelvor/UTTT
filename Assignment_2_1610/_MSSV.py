import numpy as np
import queue
from numpy.lib.twodim_base import diag
import copy
from math import inf
DEPTH = 3


def score_small_box(block, player):
    score = 0
    row_sum = np.sum(block, 1)
    col_sum = np.sum(block, 0)
    diag_sum_topleft = block.trace()
    diag_sum_topright = block[::-1].trace()
    if(any(row_sum) == player*3 + any(col_sum) == player*3 + diag_sum_topleft == player*3 + diag_sum_topright == player*3):
        score += 100
    if(any(row_sum) == player*2 + any(col_sum) == player*2 + diag_sum_topleft == player*2 + diag_sum_topright == player*2):
        score += 10
    if(any(row_sum) == player*1 + any(col_sum) == player*1 + diag_sum_topleft == player*1 + diag_sum_topright == player*1):
        score += 1
    if(any(row_sum) == player*-3 + any(col_sum) == player*-3 + diag_sum_topleft == player*-3 + diag_sum_topright == player*-3):
        score -= 100
    if(any(row_sum) == player*-2 + any(col_sum) == player*-2 + diag_sum_topleft == player*-2 + diag_sum_topright == player*-2):
        score -= 10
    if(any(row_sum) == player*-1 + any(col_sum) == player*-1 + diag_sum_topleft == player*-1 + diag_sum_topright == player*-1):
        score -= 1
    
    return score


def score(state, player):
    index_local_board = state.previous_move.x * 3 + state.previous_move.y
    score = 0
    score += score_small_box(state.blocks[index_local_board], player) * 200
    for i in range(9):
        score += score_small_box(state.blocks[i], player)
    return score


def minimax(state, depth):
    succ = []
    best_move = (-inf, None)
    valid_moves = state.get_valid_moves
    for valid_move in valid_moves:
        copyState = copy.deepcopy(state)
        copyState.act_move(valid_move)
        succ.append((copyState, valid_move))
    for s in succ:
        val = min_turn(s[0], depth-1, -inf, -inf)
        if val > best_move[0]:
            best_move = (val, s)
    return best_move[1][1]

def min_turn(state, depth, alpha, beta):
    #index_local_board = state.previous_move.x * 3 + state.previous_move.y
    if depth <= 0:#or state.global_cells[index_local_board] != 0:
        return score(state, state.player_to_move)
    succ = []
    valid_moves = state.get_valid_moves
    #print(valid_moves)
    for valid_move in valid_moves:
        copyState = copy.deepcopy(state)
        copyState.act_move(valid_move)
        succ.append((copyState, valid_move))
    for s in succ:
        val = max_turn(s[0], depth-1, alpha, beta)
        if val < beta:
            beta = val
        if alpha >= beta:
            break
    return beta


def max_turn(state, depth, alpha, beta):
    #index_local_board = state.previous_move.x * 3 + state.previous_move.y
    if depth <= 0:# or state.global_cells[index_local_board] != 0:
        return score(state, state.player_to_move)
    succ = []
    valid_moves = state.get_valid_moves
    for valid_move in valid_moves:
        copyState = copy.deepcopy(state)
        copyState.act_move(valid_move)
        succ.append((copyState, valid_move))
    for s in succ:
        val = min_turn(s[0], depth-1, alpha, beta)
        if alpha < val:
            alpha = val
        if alpha >= beta:
            break
    return alpha


def select_move(cur_state, remain_time):
    'l???y valid move ???? r???i t??nh sau'
    valid_moves = cur_state.get_valid_moves
    'l???y gi?? tr??? c???a m??nh'
    if(len(valid_moves) == 0):
        return None
    copyCur_state = copy.copy(cur_state)
    return minimax(copyCur_state, DEPTH)

    # 'valid_moves: g???m c??c ?? c?? th??? ??i ???????c, local_board, (x,y), value'
    # 'n???u value = -1, th?? c???a m??nh l?? -1, ?????ng ngh??a m??nh l?? O'
    # 'ho???c ng?????c l???i'
    # 'm??nh ??ang coi nh?? m??nh l?? -1, n???u kh??ng th?? ?????o l???i'

    # # l???y value c???a m??nh
    # #value = valid_moves[0].value
    # # c??i s??n ch??i hi???n t???i, m??nh c???n ??i???n v?? m???y v?? valid_moves trong n??y
    # localBoardNow = cur_state.blocks[valid_moves[0].index_local_board]
    # row_sum = np.sum(localBoardNow, 1)
    # col_sum = np.sum(localBoardNow, 0)
    # diag_sum_topleft = localBoardNow.trace()
    # diag_sum_topright = localBoardNow[::-1].trace()
    # 'n???u ?? n??y ???? c?? k???t qu??? th?? t??nh sau'
    # if(any(row_sum) == 3 + any(col_sum) == 3 + diag_sum_topleft == 3 + diag_sum_topright == 3):
    #     return np.random.choice(valid_moves)
    # elif(any(row_sum) == -3 + any(col_sum) == -3 + diag_sum_topleft == -3 + diag_sum_topright == -3):
    #     return np.random.choice(valid_moves)
    # # n???u ch??a c?? ai win ??? ?? local n??y
    # #print(row_sum, col_sum, diag_sum_topleft, diag_sum_topright)
    # else:
    #     return minimax(valid_moves, localBoardNow)
    return np.random.choice(valid_moves)
