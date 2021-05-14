import board
from ai import *
import time

MAINBOARD = board.Board()
SIDE = 1

root = Node(tuple(MAINBOARD.board), SIDE, 0)
tree = MinimaxTreeSearch(root, MAINBOARD)

origin_time = time.process_time()
for i in range(5):
    tree.grow(i)
    print("拓展第%s层节点耗时%ss" % (i+1, time.process_time() - origin_time))
    origin_time = time.process_time()
