import board
from ai import *
from tools import *

MAINBOARD = board.Board()
SIDE = 1

root = Node(tuple(MAINBOARD.board), SIDE, 0, "root")
Tree = ChessTree(root, MAINBOARD)