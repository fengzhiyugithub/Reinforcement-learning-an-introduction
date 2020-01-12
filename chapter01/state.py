
import numpy as np
from chapter01.common import *

# 棋盘的状态类
class State:
    # n*n 的棋盘， 1表示先手玩家, -1表示后手玩家， 0表示棋盘上该点为空
    def __init__(self):
        # 棋盘初始数据全为0， 赢家、哈希值、结束标记全为空
        self.data = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.winner = None
        self.hash_val = None
        self.end = None

    # 计算一个状态的哈希值（唯一）
    def hash(self):
        if self.hash_val is None:
            self.hash_val = 0
            for i in np.nditer(self.data):
                self.hash_val = self.hash_val * 3 + i + 1
        return self.hash_val

    # 检验是否有玩家赢得游戏或者平局
    def is_end(self):
        if self.end is not None:
            return self.end
        results = []
        # 检查行、 列
        for i in range(BOARD_ROWS):
            results.append(np.sum(self.data[i, :]))
        for j in range(BOARD_COLS):
            results.append(np.sum(self.data[:, j]))
        # 检查对角线
        trace = 0
        reverse_trace = 0
        for i in range(BOARD_ROWS):
            trace += self.data[i, i]
            reverse_trace += self.data[i, BOARD_ROWS - 1 - i]
        results.append(trace)
        results.append(reverse_trace)

        # 判断游戏赢家是先手（winner = 1）还是后手(winner = -1),修改end的值
        for result in results:
            if result == 3:
                self.winner = 1
                self.end = True
                return self.end
            if result == -3:
                self.winner = -1
                self.end = True
                return self.end
        # 判定游戏是否为平局(winner=0)
        sum_values = np.sum(np.abs(self.data))  # 棋盘上所有棋值之和
        if sum_values == BOARD_SIZE:
            self.winner = 0
            self.end = True
            return self.end

        # 游戏未结束
        self.end = False
        return self.end

    # @symbol: 1 或 -1
    # 放置一个棋子标志在(i, j)这个位置
    def next_state(self, i, j, symbol):
        new_state = State()
        new_state.data = np.copy(self.data)
        new_state.data[i, j] = symbol
        return new_state

    # 打印棋盘
    def print_state(self):
        for i in range(BOARD_ROWS):
            print('-------------')
            out = '| '
            # 根据先后手占据的位置打印相应字符
            for j in range(BOARD_COLS):
                if self.data[i, j] == 1:
                    token = '*'
                elif self.data[i, j] == -1:
                    token = 'x'
                else:
                    token = '0'
                out += token + ' | '
            print(out)
            print('-------------')