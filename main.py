import chess
import ai
from tools import *

MAIN_BOARD = chess.Board()
VERSION = 0.1
SIDE = 1


def welcome():
    """进入游戏时的欢迎语"""
    print("象棋 by Faust -v%s" % VERSION)
    print("输入 /help 可以获取帮助")


def check_movable_chess():
    """返回所有可以移动的棋子"""
    return MAIN_BOARD.get_ally_chess(1)


def input_chess(msg: str = None) -> tuple:
    """传入提示消息，使玩家输入信息，以元组形式返回玩家输入的消息"""
    ret = input(msg).split(",")
    for i in range(ret.__len__()):
        ret[i] = int(ret[i])
    return tuple(ret)


########################################################################################################################


def player_take_turn():
    """玩家对战自己"""
    global SIDE
    move_start = input_chess("你想要移动哪一颗棋子？")
    if move_start in MAIN_BOARD.get_ally_chess(SIDE):
        move_end = input_chess("要移动到哪里去？")
        MAIN_BOARD.move(move_start, move_end, confirm=True)
        SIDE = switch_side(SIDE)
    else:
        print("只能移动自己的棋子")


def bot_take_turn(level):
    global SIDE
    print("对手思考中……")
    root = ai.Node(MAIN_BOARD.board, SIDE, 0)
    tree = ai.MinimaxTreeSearch(root)
    strategy = tree.next_move(level)
    MAIN_BOARD.move(strategy[0], strategy[1], confirm=True)
    SIDE = switch_side(SIDE)


def main():
    welcome()
    level = int(input("电脑难度："))
    MAIN_BOARD.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0
            [0, 0, 0, 1, 0, 0, 0, 0, 0],  # 1
            [0, 0, 0, 0, 27, 0, 0, 0, 0],  # 2
            [0, 0, 0, 27, 0, 0, 0, 0, 0],  # 3
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4
            # 楚河  汉界
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 5
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 6
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 7
            [0, 0, 0, 0, 0, 27, 0, 0, 0],  # 8
            [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 9
        ]
    global SIDE
    SIDE = 21
    while True:
        MAIN_BOARD.print_board()
        if SIDE == 1:
            player_take_turn()
        else:
            bot_take_turn(level)


if __name__ == "__main__":
    main()
