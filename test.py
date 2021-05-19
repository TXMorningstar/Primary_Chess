import chess
from ai import *
import time

MAINBOARD = chess.Board()
SIDE = 1
LEVEL = 3

root = Node(tuple(MAINBOARD.board), SIDE, 0)
tree = MinimaxTreeSearch(root)

# origin_time = time.process_time()
# for i in range(LEVEL):
#     if i < LEVEL-1:
#         tree.grow(i)
#     else:
#         tree.grow(i, backward=True)
#     print("拓展第%s层节点耗时%ss" % (i+1, time.process_time() - origin_time))
#     origin_time = time.process_time()

ai_strategy = tree.next_move(4)
print(ai_strategy)