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


def single_vs_single():
    """玩家对战自己"""
    global SIDE
    move_start = input_chess("你想要移动哪一颗棋子？")
    if move_start in MAIN_BOARD.get_ally_chess(SIDE):
        move_end = input_chess("要移动到哪里去？")
        MAIN_BOARD.move(move_start, move_end, confirm=True)
        SIDE = switch_side(SIDE)
    else:
        print("只能移动自己的棋子")


def single_vs_bot():
    """玩家对战AI"""
    if SIDE == 1:
        single_vs_single()
    else:
        pass


def main():
    welcome()
    while True:
        MAIN_BOARD.print_board()
        single_vs_single()


if __name__ == "__main__":
    main()