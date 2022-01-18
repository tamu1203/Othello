import random
import copy
from OthelloConstant import *
from joseki import *
import OthelloLogic

kifu = ''
prev_board = None
first = None


def getRandomAction(board, moves):
    if list(f5) in moves:
        return list(f5)
    return moves[random.randrange(len(moves))]

# board:現在の盤面の状態。自分が1、相手が-1：moves:現在の合法手の一覧


def getAction(board, moves):
    global kifu, prev_board, first
    # 棋譜の作成
    if prev_board != None:
        for row in range(len(board)):
            for col in range(len(board[row])):
                if prev_board[row][col] == 0 and board[row][col] == -1:
                    # kifu += 'abcdefgh'[row] + str(col+1)
                    kifu += OthelloLogic.posToStr((col, row))
                    print(f'相手の行動を反映した棋譜は{kifu}です')
    elif first in None:
        pass
    prev_board = copy.deepcopy(board)
    s1 = 0
    for line in board:
        s1 += line.count(1)+line.count(-1)
    if s1 == 4:
        return list(f5)

    for joseki in josekis:
        # josekiがkifuから始まるときtrue
        if joseki.startswith(kifu):
            # startswith(kifu)で一致していて、定石がそこで切れる場合は桁数が同じになるためイコール
            if len(kifu) == len(joseki):
                continue
            ret = list(eval(joseki[len(kifu):len(kifu)+2]))
            kifu += joseki[len(kifu):len(kifu)+2]
            print(f'自分の刺し手を追加した棋譜は{kifu}')
            print(f'定石の{joseki}を使いました( ´•̥̥̥ω•̥̥̥` )')
            print(f'{OthelloLogic.posToStr(ret)}を打ちました')
            return ret
    # exit()
    return moves[random.randrange(len(moves))]


"""
getAction仕様書
保持する変数の値
    これまでの棋譜を'f5d6c5f4e3'のような値で保持する
        実現方法:
            毎回boardの差分を確認して、毎回"+="することで保持する
            前回0だった場所で1に変化した場所を加える

    これまでの棋譜と定石を比較し、定石に当てはまる場合はその定石の続きを入力する。
    定石にあてはまらなくなった場合は、棋譜を保持するのを辞め、alpha-beta法で最善手を求めて返却する
"""
