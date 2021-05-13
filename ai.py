# class Node(object):
#     """节点对象"""
#
#     def __init__(self, board: tuple, side: int, price: int, *args, location: "str" = None, parent: object = None):
#         self.board = board
#         self.side = side
#         self.price = price
#         self.parent = parent
#         self.locator = location
#         self.leaf = list(args)  # 在这里存储它的子节点
#
#
# class Tree(object):
#     """树管理器"""
#     def __init__(self, board: tuple, side: int, price: int):
#         self.tree = Node(board, side, price)  # 创建根节点
#         self.members = [self.tree]
#         self.depth = 0
#
#     def get_node_by_level(self, level):
#         for i in range
#
#
#     def expand(self):
#         pass
#
#     def grow(self):


from copy import deepcopy
from tools import *


class Node(object):
    """节点对象"""

    def __init__(self, board: tuple, side: int, price: int, location: str = None):
        self.board = board
        self.side = side
        self.price = price
        self.location = location


class Tree(object):
    """树的列表实现"""

    def __init__(self):
        self.tree = ["root"]

    def get_node(self, location: str, leaf: bool = False):
        """获取某个节点"""
        node = self.tree
        if location:  # 防止请求根节点
            for i in location:
                node = node[int(i)]  # 索引至树

        if leaf:
            return node
        return node[0]

    def get_node_by_level(self, level: int, leaf: bool = False) -> list:
        """传入层数获取某一层的节点"""
        result = list()  # 储存结果
        next_search = [deepcopy(self.tree)]  # 储存搜索过程中找到的叶节点

        for i in range(level + 1):
            search = next_search.copy()
            next_search = list()

            # 如果是其它层，那么去掉头，将剩余部分放入待探索列表即可
            if i != level:
                for node in search:
                    node.pop(0)
                    next_search.extend(node)

            # 如果是目标层，那么把头放进结果列表即可
            else:
                for node in search:
                    if leaf:
                        result.append(node)
                    else:
                        result.append(node[0])
        return result

    def insert_node(self, node: object, location: str = "") -> str:
        """在树的指定位置插入一个节点，返回节点的定位符"""
        # 获取需要插入节点的位置
        parent = self.get_node(location, leaf=True)
        # 插入节点
        parent.append([node])
        # 更新节点定位符信息
        child_location = location + repr(parent.__len__() - 1)
        node.location = child_location
        return child_location

    def del_node(self, location: str = ""):
        """通过定位符删除节点
        删除节点会造成定位符混乱，应尽量避免使用此方法
        说明：找到父节点后，再使用pop方法删除掉指定的节点"""
        if location == "":
            self.tree = list()
            return

        node = self.get_node(location[:-1], True)
        node.pop(int(location[-1]))


class ChessTree(Tree):
    def __init__(self, root: object, board_obj: object):
        self.tree = [root]
        self.board_obj = board_obj
        self.depth = 0

    def analyze(self, node: object) -> tuple:
        """该方法会返回节点下所有可以行动的策略"""
        strategy = list()
        ally_chess = self.board_obj.get_ally_chess(node.side, node.board)
        for chess in ally_chess:  # 依次扫描每个棋子的可落子点
            movable_pos = self.board_obj.movable(chess, node.board, price=True)
            for pos in movable_pos:  # 解包
                x, y, price = pos
                strategy.append((chess, (x, y), price))  # 将落子点与棋子都存入战略表中
        return tuple(strategy)

    def expand(self, parent_node: object, strategy: tuple) -> bool:
        """调用该方法后会根据传入的战略表拓展节点"""
        start_pos, dest_pos, price = strategy  # 解包
        board = self.board_obj.move(start_pos, dest_pos, board=parent_node.board)  # 计算衍生出的新棋盘
        side = switch_side(parent_node.side)  # 切换回合
        child_node = Node(board, side, price)  # 生成子节点
        self.insert_node(child_node, parent_node.location)  # 将新的节点插入进树中


    def grow(self):
        """调用这个方法后，树会自动解析节点并向下延伸一层新的叶节点"""
        new_node = self.get_node_by_level(self.depth)  # 获取一层内的所有节点
        # 扫描所有可落子点
        for node in new_node:  # 依次扫描new_code中的节点的友方棋子
            strategy = self.analyze(node)
            for step in strategy:
                self.expand(node, step)

        self.depth += 1
