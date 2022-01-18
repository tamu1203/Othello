import copy
import numpy as np
from OthelloConstant import d3, c4, e6, f5


def execute(board, action, player, size):

    dirs = [
        [-1, -1],
        [0, -1],
        [1, -1],
        [-1, 0],
        [1, 0],
        [-1, 1],
        [0, 1],
        [1, 1]
    ]
    board[action[1]][action[0]] = player
    for dir in dirs:
        bool, flips = executeFlip(
            board, player, action[1], action[0], dir, size)
        if bool:
            for flip in flips:
                board[flip[0]][flip[1]] = player
    return board


def executeFlip(b, p, x, y, dir, size):
    if x+dir[0] < 0 or x+dir[0] >= size or y+dir[1] < 0 or y+dir[1] >= size:
        return 0, None

    if b[x+dir[0]][y+dir[1]] == p*-1:
        flips = []
        flips.append([x+dir[0], y+dir[1]])
        inc_dir = [dir[0], dir[1]]
        inc_dir[0] += dir[0]
        inc_dir[1] += dir[1]
        while True:
            if x+inc_dir[0] < 0 or x+inc_dir[0] >= size or y+inc_dir[1] < 0 or y+inc_dir[1] >= size:
                return 0, None

            if b[x+inc_dir[0]][y+inc_dir[1]] == p:
                return 1, flips
            elif b[x+inc_dir[0]][y+inc_dir[1]] == 0:
                return 0, None

            flips.append([x+inc_dir[0], y+inc_dir[1]])
            inc_dir[0] += dir[0]
            inc_dir[1] += dir[1]

    return 0, None


def getMoves(board, player, size):
    dirs = [
        [-1, -1],
        [0, -1],
        [1, -1],
        [-1, 0],
        [1, 0],
        [-1, 1],
        [0, 1],
        [1, 1]
    ]
    moves = []
    for y in range(size):
        for x in range(size):
            if board[x][y] == (player*-1):
                for dir in dirs:
                    legal_move = search(player, board, x, y, dir, size)
                    if legal_move and not(legal_move in moves):
                        moves.append(legal_move)
    return moves


def search(p, b, x, y, dir, size):
    if x+dir[0] < 0 or x+dir[0] >= size or y+dir[1] < 0 or y+dir[1] >= size:
        return None

    if b[x+dir[0]][y+dir[1]] == 0:
        reverse_dir = [dir[0]*-1, dir[1]*-1]
        while(True):
            if x+reverse_dir[0] < 0 or x+reverse_dir[0] >= size or y+reverse_dir[1] < 0 or y+reverse_dir[1] >= size:
                return None

            if b[x+reverse_dir[0]][y+reverse_dir[1]] == p:
                return [y+dir[1], x+dir[0]]
            elif b[x+reverse_dir[0]][y+reverse_dir[1]] == 0:
                return None

            reverse_dir[0] += dir[0]*-1
            reverse_dir[1] += dir[1]*-1

    return None


def getReverseboard(board):
    rev_board = copy.deepcopy(board)
    for x in range(len(rev_board)):
        for y in range(len(rev_board)):
            rev_board[x][y] *= -1
    return rev_board


def printBoard(board):

    for y in board:
        row = ''
        for x in y:
            # cell = '○ ' if x == 1 else '● ' if x == -1 else '  '
            # 0だったら空白、1だったらO、-1だったらX
            cell = 'O ' if x == 1 else 'X ' if x == -1 else '  '
            row += cell
        print(row)


def posToStr(pos):
    return 'abcdefgh'[pos[0]] + str(pos[1]+1)


def convertBoard(first, board):
    if first == d3:
        # 左右反転のfliplrで実質的に上下反転
        return np.fliplr(np.rot90(board))
    if first == c4:
        # 右に180度回転
        return np.rot90(board, 2)
    if first == e6:
        # 上下反転のfliplrで実質的に左右反転
        return np.flipud(np.rot90(board))
    if first == f5:
        return board
    assert False