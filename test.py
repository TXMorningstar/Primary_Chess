import board
from ai import *
import time

MAINBOARD = board.Board()
SIDE = 1

root = Node(tuple(MAINBOARD.board), SIDE, 0)
tree = MinimaxTreeSearch(root, SIDE, MAINBOARD)

origin_time = time.process_time()
for i in range(4):
    node_len = tree.grow(i)
    print("拓展第%s层节点耗时%ss" % (i+1, time.process_time() - origin_time))
    origin_time = time.process_time()

tree.get_node_by_level(4)
print("遍历第4层节点耗时%ss" % (time.process_time() - origin_time))