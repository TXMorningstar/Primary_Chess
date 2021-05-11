import board
from ai import *
from tools import *

MAIN_BOARD = board.Board()
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
    move_start = input_chess("你想要移动哪一颗棋子？")
    if move_start in MAIN_BOARD.get_ally_chess(SIDE):
        move_end = input_chess("要移动到哪里去？")
        MAIN_BOARD.move(move_start, move_end)
        switch_side(SIDE)
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
















# import game
# import sys
#
#
# VERSION = 0.1
# chess_game = game.Board()
# side = "red"
#
#
# def cutting_line():
#     """没什么意义的分割线"""
#     print("-----" * 30)
#
#
#
#
# def help():
#     """打印帮助信息，包含玩家指令及用法"""
#     print("=" * 20, "帮助", "=" * 20)
#
#
# def new_game():
#     """使用此方法开始新游戏"""
#     global chess_game
#     chess = game.Board()
#
#
# def new_turn():
#     """使用此方法开始新回合"""
#
#
# def surrender():
#     """使用此方法时执子方投降"""
#     pass
#
#
# def exit_game(confirm=[]):
#     """退出游戏"""
#     def inner():
#         if confirm:
#             sys.exit()
#         else:
#             confirm.append(True)
#             print("你确认要退出吗，确认请输入/exit")
#     return inner
#
#
# def command(cmd):
#     """处理玩家命令"""
#     exit = exit_game()
#     response = {
#         "/new game": new_game,
#         "/surrender": surrender,
#         "/exit": exit
#     }
#     if "/" in cmd:
#         if cmd != "/exit":
#             exit(confirm=[])
#         return response[cmd]()
#     else:
#         pass
#
#
# def main():
#     welcome()
#     while True:
#         ret = command(input("请输入命令>> "))
#         if ret:
#             chess_game.print_board()
#
# if __name__ == "__main__":
#     main()
