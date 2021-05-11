from tools import *


class Board(object):
    """这个类包含中国象棋游戏棋盘、棋子和各种方法"""

    def __init__(self):
        """初始化类"""
        # 生成棋盘
        self._generate_board()

        # 映射表，黑小在上，红大在下，命令行打印用
        self.mapping = {
            0: "·",
            1: "将",
            2: "士",
            3: "象",
            4: "馬",
            5: "車",
            6: "砲",
            7: "兵",
            21: "帥",
            22: "仕",
            23: "相",
            24: "傌",
            25: "俥",
            26: "炮",
            27: "卒"
        }

        # 九宫，用(x, y) in self.palace判断是否在九宫内
        self.palace = [
            (0, 3), (0, 4), (0, 5),
            (1, 3), (1, 4), (1, 5),
            (2, 3), (2, 4), (2, 5),
            # 楚河 汉界
            (7, 3), (7, 4), (7, 5),
            (8, 3), (8, 4), (8, 5),
            (9, 3), (9, 4), (9, 5)
        ]
        self.king_strategy = ((0, 1), (1, 0), (-1, 0), (0, -1))
        self.guard_strategy = ((1, 1), (-1, -1), (1, -1), (-1, 1))
        self.minister_strategy = ((2, 2), (-2, -2), (2, -2), (-2, 2))
        self.horse_strategy = (
            ((-1, 0), ((-1, -1), (-1, 1))),  # 上
            ((0, 1), ((-1, 1), (1, 1))),  # 右
            ((1, 0), ((1, -1), (1, 1))),  # 下
            ((0, -1), ((-1, -1), (1, -1)))  # 左
        )
        self.chariot_strategy = ((-1, 0), (0, -1), (1, 0), (0, 1))
        self.pawn_strategy = {27: (-1, 0), 7: (1, 0)}
        self.pawn_strategy_crossed = {27: ((-1, 0), (0, -1), (0, 1)), 7: ((1, 0), (0, -1), (0, 1))}

    def _generate_board(self):
        """生成棋盘"""
        self.board = [
            [5, 4, 3, 2, 1, 2, 3, 4, 5],  # 0
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1
            [0, 6, 0, 0, 0, 0, 0, 6, 0],  # 2
            [7, 0, 7, 0, 7, 0, 7, 0, 7],  # 3
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4
            # 楚河  汉界
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 5
            [27, 0, 27, 0, 27, 0, 27, 0, 27],  # 6
            [0, 26, 0, 0, 0, 0, 0, 26, 0],  # 7
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 8
            [25, 24, 23, 22, 21, 22, 23, 24, 25]  # 9
        ]
        self.history = list()

    def _update_board(self, board: tuple, history_board: tuple) -> bool:
        """将棋盘更新为传入的新棋盘"""
        self.board = board
        self.history.append(history_board)
        return True

    def print_board(self, board: tuple = None):
        """打印棋盘，可传入指定棋盘"""
        if not board:
            board = self.board
        times = 0
        print("".ljust(4), end="")
        for i in range(9):
            print("%s".ljust(5) % i, end="")
        print("\n")
        for x in board:
            times += 1
            print("%s".ljust(4) % (times - 1), end="")
            for y in x:
                if y == 0:
                    print(self.mapping[y], end="  ")
                elif y < 10:
                    cprint(self.mapping[y], "red", "yellow", end="  ")
                else:
                    cprint(self.mapping[y], "black", "yellow", end="  ")
            print("\n")
            if times == 5:
                print("            楚河        汉界\n")

    def print_board_raw(self, board: tuple = None):
        """打印棋盘上的数据"""
        if not board:
            board = self.board
        for x in board:
            for y in x:
                print(y, end="  ")
            print("\n")

    @staticmethod
    def inside_board(pos: tuple) -> bool:
        """检查某个点是否在棋盘内"""
        if 9 >= pos[0] >= 0 and 8 >= pos[1] >= 0:
            return True

    def not_ally_chess(self, pos: tuple, expo_pos: tuple, board: tuple = None) -> bool:
        """传入棋子原坐标和探索点坐标，检查棋盘坐标点内棋子是否为有方"""
        if not board:
            board = self.board
        if 0 < abs(board[pos[0]][pos[1]] - board[expo_pos[0]][expo_pos[1]]) >= 10 or board[expo_pos[0]][
            expo_pos[1]] == 0:
            return True  # 不为己方棋子

    def get_ally_chess(self, king: int, board: tuple = None) -> tuple:
        """获取所有友方棋子的坐标。传入己方将的数值代表方向，可选择传入指定的棋盘。返回一个元组包含所有棋子的坐标"""
        if not board:
            board = self.board
        ally_chess = {1: (1, 2, 3, 4, 5, 6, 7), 21: (21, 22, 23, 24, 25, 26, 27)}  # 一个字典，包含将对应友方棋子的set
        result = list()
        x, y = 0, 0

        # 扫描棋盘寻找棋子
        for x_value in board:
            for y_value in x_value:
                if y_value in ally_chess[king]:
                    result.append((x, y))
                y += 1
            x += 1
            y = 0
        return tuple(result)

    def get_chess_pos(self, chess: int, board: tuple = None) -> tuple:
        """传入一个棋子种类，可选择传入指定的棋盘。返回所有此种类棋子的坐标"""
        if not board:
            board = self.board
        result = list()
        x, y = 0, 0

        # 扫描棋盘寻找棋子
        for x_value in board:
            for y_value in x_value:
                if y_value == chess:
                    result.append((x, y))
                y += 1
            x += 1
            y = 0
        return tuple(result)

    def king_meet(self, board: tuple = None) -> bool:
        """检查棋盘，可选择传入指定的棋盘，如果棋盘内发生老王见面则返回True"""
        if not board:
            board = self.board
        # 寻找双方将，若无法找到一方的将，则会发出警告并返回假
        try:
            red_king = self.get_chess_pos(1, board)[0]
            black_king = self.get_chess_pos(21, board)[0]
        except IndexError:
            print("Error: 缺少将")
            return False
        # 如果双方王的y轴不一致，则一定不可能相遇
        if red_king[1] != black_king[1]:
            return False
        # 在双方王y一致的情况下，需要从红方王开始自上而下检查棋盘，如果在没有任何遮挡物的情况下发现敌方王则返回真
        y = red_king[1]
        x = 0
        while True:  # 不需要使用for
            x += 1
            if board[x][y] == 0:
                continue
            elif board[x][y] == 21:
                return True
            else:
                return False

    def cross_river(self, pos: tuple, expo_pos: tuple) -> bool:
        """传入一个棋子的坐标以及探索点坐标，返回探索点位置是否过河"""
        x, y, ex, ey = pos[0], pos[1], expo_pos[0], expo_pos[1]
        if self.board[x][y] <= 10:
            if ex <= 4:  # 棋子为1~7, 5,6,7,8,9过河
                return False
            else:
                return True
        else:  # 棋子为21~27, 4,3,2,1,0过河
            if ex >= 5:
                return False
            else:
                return True

    def check_chess_type_by_pos(self, pos: tuple, *args: int, board: tuple = None) -> bool:
        if not board:
            board = self.board
        """检查某个坐标点上的棋子是否为传入的参数,可以传入任意数量的参数"""
        if board[pos[0]][pos[1]] in args:
            return True
        else:
            return False

    def movable(self, pos: tuple, board: tuple = None, price: bool = False) -> tuple:
        """获取某个棋子可以移动的范围，随后调用对应的方法"""
        chess = self.board[pos[0]][pos[1]]
        print("选择的棋子:", self.mapping[chess])
        function_map = {
            1: self.king,
            21: self.king,
            2: self.guard,
            22: self.guard,
            3: self.minister,
            23: self.minister,
            4: self.horse,
            24: self.horse,
            5: self.chariot,
            25: self.chariot,
            6: self.cannon,
            26: self.cannon,
            7: self.pawn,
            27: self.pawn
        }
        if not self.check_chess_type_by_pos(pos, 0):
            return function_map[chess](pos, board=board, price=price)

    def king(self, pos: tuple, board: tuple = None, price: bool = False) -> tuple:
        """将的行走规则"""
        if not board:
            board = self.board
        x, y = pos
        result = list()  # 用于存储搜索结果，结果储存在一个列表中，在方法最后返回结果

        # 循环检查将的可落子点
        for strategy in self.king_strategy:
            ex, ey = x + strategy[0], y + strategy[1]  # 更新探索点的坐标

            if self.inside_board((ex, ey)):  # 检查坐标点是否合
                if self.not_ally_chess((x, y), (ex, ey), board):  # 无己方棋子
                    if (ex, ey) in self.palace:  # 结果在九宫内
                        if price:
                            result.append((ex, ey, board[ex][ey]))  # 将结果加入元组准备返回
                        else:
                            result.append((ex, ey))
        return tuple(result)

    def guard(self, pos: tuple, board: tuple = None, price: bool = False) -> tuple:
        """仕的行走规则"""
        if not board:
            board = self.board
        x, y = pos
        result = list()

        for strategy in self.guard_strategy:
            ex, ey = x + strategy[0], y + strategy[1]  # 更新探索点
            if self.inside_board((ex, ey)):  # 检查坐标点是否在棋盘内
                if self.not_ally_chess((x, y), (ex, ey), board):  # 检查己方棋子
                    if (ex, ey) in self.palace:  # 检查是否在九宫格内
                        if price:
                            result.append((ex, ey, board[ex][ey]))  # 将结果加入元组准备返回
                        else:
                            result.append((ex, ey))
        return tuple(result)

    def minister(self, pos: tuple, board: tuple = None, price: bool = False) -> tuple:
        """相的行走规则"""
        x, y = pos
        result = list()

        for strategy in self.minister_strategy:
            ex, ey = x + strategy[0], y + strategy[1]  # 更新探索点
            if self.inside_board((ex, ey)):
                if self.not_ally_chess((x, y), (ex, ey), board):
                    if not self.cross_river(pos, (ex, ey)):
                        if price:
                            result.append((ex, ey, board[ex][ey]))  # 将结果加入元组准备返回
                        else:
                            result.append((ex, ey))
        return tuple(result)

    def horse(self, pos: tuple, board: tuple = None, price: bool = False) -> tuple:
        """馬的行走规则"""
        if not board:
            board = self.board
        x, y = pos
        # 马的规则更为复杂，可以拆开理解为两步：首先向目标位置前进一步，然后再向斜方向走一步
        # 因此，马的行走规则分为两步
        # 下面的元组分为两层：第一层为四个主要搜索策略（上下左右），第二层为第一次和第二次的搜索方向
        result = list()

        for strategy in self.horse_strategy:  # 第一层
            ex, ey = x + strategy[0][0], y + strategy[0][1]
            if self.inside_board((ex, ey)):
                if self.not_ally_chess((x, y), (ex, ey), board):
                    # 第一次搜索完成，撇脚马排除
                    for i in range(2):  # 接下来需要进行两次叶节点检查，i代表检查的方向
                        ex_nd, ey_nd = ex + strategy[1][i][0], ey + strategy[1][i][1]  # 根据上一个探索点的位置赋值下一个探索点
                        if self.inside_board((ex, ey)):
                            if self.not_ally_chess((x, y), (ex_nd, ey_nd), board):
                                if price:
                                    result.append((ex, ey, board[ex][ey]))  # 将结果加入元组准备返回
                                else:
                                    result.append((ex, ey))
        return tuple(result)

    def chariot(self, pos: tuple, board: tuple = None, price: bool = False) -> tuple:
        """車的行走规则"""
        if not board:
            board = self.board
        x, y = pos
        result = list()

        for strategy in self.chariot_strategy:  # 一共四个移动方向
            ex, ey = x, y  # 初始化最初的ex,ey值，因为while里会进行赋值，所以在这里直接赋值等于x，y就行了
            while True:  # 向一个移动方向不断寻找
                ex, ey = ex + strategy[0], ey + strategy[1]  # 更新探索点
                if self.inside_board((ex, ey)):
                    if self.not_ally_chess((x, y), (ex, ey), board):
                        if price:  # 如果不是则加入结果
                            result.append((ex, ey, board[ex][ey]))
                        else:
                            result.append((ex, ey))
                        if self.check_chess_type_by_pos((ex, ey), 0, board=board):  # 如果探索点为空，则继续探索
                            continue
                    # 如果搜索路径上遇到任何障碍则立即停止搜索并开启下一个方向的搜索
                break
        return tuple(result)

    def cannon(self, pos: tuple, board: tuple = None, price: bool = False) -> tuple:
        """炮的行走规则"""
        if not board:
            board = self.board
        x, y = pos
        # 炮的移动几乎与車一样，不过炮在攻击时需要隔一个地方棋子
        result = list()

        for strategy in self.chariot_strategy:  # 一共四个移动方向
            ex, ey = x, y  # 初始化最初的ex,ey值，因为while里会进行赋值，所以在这里直接赋值等于x，y就行了
            while True:  # 向一个移动方向不断寻找
                ex, ey = ex + strategy[0], ey + strategy[1]  # 更新探索点
                if self.inside_board((ex, ey)):
                    if self.check_chess_type_by_pos((ex, ey), 0, board=board):
                        result.append((ex, ey, board[ex][ey]))
                        continue  # 如果探索点为空，则进行下一次搜索
                    else:  # 探索点发现棋子，这个棋子无法吃掉，我们需要跳过它进行第二次搜索
                        while True:
                            ex, ey = ex + strategy[0], ey + strategy[1]  # 更新探索点，跳过刚才的探索点
                            if self.inside_board((ex, ey)):
                                if self.check_chess_type_by_pos((ex, ey), 0, board=board):  # 如果探索点是空棋子，可以继续搜索
                                    continue
                                elif self.not_ally_chess((x, y), (ex, ey),
                                                         board):  # 虽然not_ally_chess包含0的结果，但通过elif依然可以正确执行
                                    if price:
                                        result.append((ex, ey, board[ex][ey]))
                                    else:
                                        result.append((ex, ey))
                            break
                # 如果搜索路径上遇到任何障碍则立即停止搜索并开启下一个方向的搜索
                break
        return tuple(result)

    def pawn(self, pos: tuple, board: tuple = None, price: bool = False) -> tuple:
        """卒的行走规则"""
        if not board:
            board = self.board
        x, y = pos
        # 卒的特殊之处在于卒在过河前和过河后的行走规则差别非常大，根据这个特性可以尝试先判断再搜索
        # 同时，对卒来说还有“前后”一说，需要分开讨论，具体实现为创建一个字典对应两个不同的策略
        chess = board[x][y]  # 找到棋子的具体数值，根据它来决定移动策略
        result = list()

        if self.cross_river((x, y), (x, y)):  # 过河后
            for strategy in self.pawn_strategy_crossed[chess]:
                ex, ey = x + strategy[0], y + strategy[1]
                if self.inside_board((ex, ey)):
                    if self.not_ally_chess((x, y), (ex, ey), board):
                        if price:
                            result.append((ex, ey, board[ex][ey]))
                        else:
                            result.append((ex, ey))
        else:
            ex, ey = x + self.pawn_strategy[chess][0], y + self.pawn_strategy[chess][1]
            if self.inside_board((ex, ey)):
                if self.not_ally_chess((x, y), (ex, ey), board):
                    if price:
                        result.append((ex, ey, board[ex][ey]))
                    else:
                        result.append((ex, ey))
        return tuple(result)

    def move(self, start: tuple, end: tuple, confirm: bool = False, board: tuple = None) -> tuple:
        """移动某个棋子，并返回移动棋子后的棋盘。传入参数：棋子坐标，目标坐标，是否更新实例对象中的棋盘，要使用的棋盘"""
        if not board:
            board = self.board
        new_board = self.board

        if end in self.movable(start, board):
            new_board[start[0]][start[1]], new_board[end[0]][end[1]] = 0, board[start[0]][start[1]]  # 更新新棋盘的数组
            if confirm:
                self._update_board(new_board, board)
            return new_board
        else:
            raise ValueError("无法移动这个棋子")

    def judge(self) -> bool:
        """判断玩家是否获胜。可选择传入指定的棋盘。返回一个布尔值，真代表当前执子方获胜"""
        # 检查双方将是否存在
        # 王见面最后判定
        if self.king_meet():  # 若在执子方回合发生王见面，则执子方落败
            return False
