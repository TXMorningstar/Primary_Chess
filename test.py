import chess
from ai import *
import time

MAINBOARD = chess.Board()
SIDE = 1

root = Node(tuple(MAINBOARD.board), SIDE, 0)
tree = MinimaxTreeSearch(root)

origin_time = time.process_time()
for i in range(3):
    if i != 2:
        tree.grow(i)
    else:
        tree.grow(i, final=True)
    print("拓展第%s层节点耗时%ss" % (i+1, time.process_time() - origin_time))
    origin_time = time.process_time()
print("完成")