from copy import copy
from chess import Board
from tools import *


class Node(object):
    """节点对象"""

    def __init__(self, board: tuple, side: int, value: int, self_value: int = 0, strategy: tuple = tuple(), location: list = list()):
        self.board = board
        self.side = side
        self.self_value = self_value
        self.value = value
        self.location = copy(location)
        self.strategy = strategy

    def __repr__(self):
        return str(self.self_value)


class Tree(object):
    """树的列表实现"""

    def __init__(self, root):
        self.tree = [root]

    def get_node(self, location: list, ret_list: bool = False):
        """获取某个节点"""
        node = self.tree
        if location:  # 防止请求根节点
            for i in location:
                node = node[i]  # 索引至树

        if ret_list:
            return node
        return node[0]

    def get_node_by_level(self, level: int, leaf: bool = False) -> list:
        """传入层数获取某一层的节点"""
        result = list()  # 储存结果
        search, next_search = [self.tree], [self.tree]  # 储存搜索过程中找到的叶节点

        # 搜索最后一层
        for i in range(level):
            search = next_search
            next_search = list()

            for node in search:
                next_search.extend(node[1:])

        if leaf:
            return next_search
        else:
            for node in next_search:
                result.append(node[0])
            return result

    def insert_node(self, node: object, location: list = "") -> list:
        """在树的指定位置插入一个节点，返回节点的定位符"""
        # 获取需要插入节点的位置
        parent = self.get_node(location, ret_list=True)
        # 插入节点
        # noinspection PyTypeChecker
        parent.append([node])
        # 更新节点定位符信息
        child_location = copy(location)
        child_location.append(parent.__len__() - 1)
        node.location = child_location
        return child_location


class MinimaxTreeSearch(Tree):
    """基于列表树的MiniMax Tree Search算法"""

    def __init__(self, root: Node):
        super().__init__(root)
        self.board_obj = Board()
        self.depth = 0
        self.side = root.side

    def analyze(self, node: Node) -> tuple:
        """该方法会返回节点下所有可以行动的策略"""
        strategy = list()
        ally_chess = self.board_obj.get_ally_chess(node.side, node.board)
        for chess in ally_chess:  # 依次扫描每个棋子的可落子点
            movable_pos = self.board_obj.movable(chess, node.board, price=True)
            for pos in movable_pos:  # 解包
                x, y, price = pos
                strategy.append((chess, (x, y), price))  # 将落子点与棋子都存入战略表中
        return tuple(strategy)

    def expand(self, parent_node: Node, strategy: tuple):
        """调用该方法后会根据传入的战略表拓展节点"""
        start_pos, dest_pos, price = strategy  # 解包
        board = self.board_obj.move(start_pos, dest_pos, board=parent_node.board)  # 计算衍生出的新棋盘
        side = switch_side(parent_node.side)  # 切换该节点的回合
        price = self.price_estimate(price, dest_pos[0])  # 生成一个更可信的价值
        reward = price + parent_node.value
        child_node = Node(board, side, reward, self_value=price, strategy=(start_pos, dest_pos))  # 生成子节点
        self.insert_node(child_node, parent_node.location)  # 将新的节点插入进树中

    def grow(self, level, backward: bool = False):
        """调用这个方法后，树会自动解析节点并向下延伸一层新的叶节点"""
        new_node = self.get_node_by_level(level, leaf=True)  # 获取一层内的所有节点
        # 扫描所有可落子点
        for node in new_node:  # 依次扫描new_code中的节点的友方棋子
            strategy = self.analyze(node[0])  # 生成战略表
            for step in strategy:
                self.expand(node[0], step)  # 根据战略表拓展树
            if backward:
                self.value_backward(node)  # 调用反向传播算法，向父节点传递
        self.depth += 1

    def next_move(self, depth: int) -> tuple:
        """调用这个方法后，返回一个ai计算出的战略表"""
        depth -= 1
        for i in range(depth):
            self.grow(i)
        self.grow(depth, backward=True)
        for i in range(depth-1):
            self.level_backward(depth)
            depth -= 1
        return self.final_select()

    def final_select(self) -> tuple:
        """根据第一层节点的价值选择"""
        nodes_list = self.get_node_by_level(1)
        max_value = -1024
        max_value_location = 1
        node_location = 0
        for node in nodes_list:
            if node.value >= max_value:
                max_value = node.value
                max_value_location = node_location
            node_location += 1
        return nodes_list[max_value_location].strategy

    def value_backward(self, parent_tree: list) -> int:
        """根据传入的父节点，将它的子节点价值传回父节点，修改父节点的价值"""
        value_set = list()
        if parent_tree.__len__() <= 1:
            return parent_tree[0].value
        for node in parent_tree:
            if type(node) != list:
                parent = node
            else:
                value_set.append(node[0].value)
        # Mini or Max
        if parent.side != self.side:
            value = min(value_set)
            method = "min"
        else:  # 否则，取最小值向上传递
            value = max(value_set)
            method = "max"
        parent.value = value
        parent.select = value
        parent.method = method
        return value

    def level_backward(self, level):
        """传入一个整型，将这一层的价值传递给它们的父节点"""
        parents_list = self.get_node_by_level(level-1, leaf=True)  # 获得所有的父节点
        for parent in parents_list:
            self.value_backward(parent)

    @staticmethod
    def _pawn_value(xpos: int, negative: bool = False) -> int:
        # reverse代表正在被计算的棋子是一颗自己的棋子
        if negative:
            if xpos <= 4:
                return -1
            else:
                return -3
        else:
            if xpos <= 4:
                return 3
            else:
                return 1

    def price_estimate(self, chess: int, xpos: int) -> int:
        """调用这个方法后，返回一个更可信的价值
        不过无论再可信也只不过是一个Naive value罢了"""
        # 卒价值1(未过河)/3(过河)，其它不可过河单位价值2，可过河单位价值4，将价值100
        price_map = {
            1: {0: 0,
                1: -200,
                2: -2,
                3: -2,
                4: -4,
                5: -4,
                6: -4,
                7: self._pawn_value(xpos, negative=True),
                21: 100,
                22: 2,
                23: 2,
                24: 4,
                25: 4,
                26: 4,
                27: self._pawn_value(xpos)
                },

            21: {0: 0,
                 21: -200,
                 22: -2,
                 23: -2,
                 24: -4,
                 25: -4,
                 26: -4,
                 27: self._pawn_value(xpos, negative=True),
                 1: 100,
                 2: 2,
                 3: 2,
                 4: 4,
                 5: 4,
                 6: 4,
                 7: self._pawn_value(xpos)
                 },
        }
        return price_map[self.side][chess]

    # TODO: Alpha-Beta Pruning
