from chapter01.common import *
from chapter01.get_all_states import all_states
import numpy as np
import pickle
import warnings
warnings.filterwarnings("ignore")

'''
        V(St) ← V(St) + α * [ V(St+1) − V(St) ]，
        α 是步长，两个连续时间的St估计值的差（即V(St+1)−V(St)）
        St 表示贪婪移动之前的状态，而 St+1 表示移动之后的状态
'''
# AI player
class Player:
    # @step_size: 用于更新estimations的步长
    # @epsilon: 探索的概率
    def __init__(self, step_size=0.1, epsilon=0.1):
        self.estimations = dict()
        self.step_size = step_size
        self.epsilon = epsilon
        self.states = []
        self.greedy = []
        self.symbol = 0

    def reset(self):
        self.states = []
        self.greedy = []

    # 设置状态
    def set_state(self, state):
        self.states.append(state)
        self.greedy.append(True)

    # 设置标志symbol
    def set_symbol(self, symbol):
        self.symbol = symbol
        for hash_val in all_states:
            # state指当前棋局的状态， is_end表示结束标志
            state, is_end = all_states[hash_val]
            # 游戏结束
            if is_end:
                # 当前棋手赢棋
                if state.winner == self.symbol:
                    self.estimations[hash_val] = 1.0
                # 平局
                elif state.winner == 0:
                    self.estimations[hash_val] = 0.5
                # 当前棋手输棋
                else:
                    self.estimations[hash_val] = 0
            # 游戏未结束
            else:
                self.estimations[hash_val] = 0.5

    # 更新值估计
    def backup(self):
        states = [state.hash() for state in self.states]
        #  V(St) ← V(St) + α * [ V(St+1) − V(St) ]
        #  td_error 即为 α * [ V(St+1) − V(St) ]， self.estimations[state] 即为 V(St)
        for i in reversed(range(len(states) - 1)):
            state = states[i]
            td_error = self.greedy[i] * (
                    self.estimations[states[i + 1]] - self.estimations[state]
            )
            self.estimations[state] += self.step_size * td_error

    # 基于现在的状态选择一个动作
    def act(self):
        state = self.states[-1]
        next_states = []
        next_positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if state.data[i, j] == 0:
                    # 棋手放置一个棋子在[i, j]处 并 将新状态的哈希值（唯一）添加至 next_states中
                    next_positions.append([i, j])
                    next_states.append(state.next_state(
                        i, j, self.symbol).hash())
        # 以小于 epsilon 的概率探索
        if np.random.rand() < self.epsilon:
            # 任选一个 next_positions[ [0, len(next_positions)) ] 位置落子
            action = next_positions[np.random.randint(len(next_positions))]
            action.append(self.symbol)
            self.greedy[-1] = False
            return action

        values = []
        for hash_val, pos in zip(next_states, next_positions):
            values.append((self.estimations[hash_val], pos))
        # 将values随机排列， 这里是否可省？?
        np.random.shuffle(values)
        # 按values第一个关键字 即hash_val 降序排列
        values.sort(key=lambda x: x[0], reverse=True)
        action = values[0][1]
        action.append(self.symbol)
        return action

    # 保存策略(二进制格式）
    def save_policy(self):
        with open('policy_%s.bin' % ('first' if self.symbol == 1 else 'second'), 'wb') as f:
            pickle.dump(self.estimations, f)

    # 加载策略
    def load_policy(self):
        with open('policy_%s.bin' % ('first' if self.symbol == 1 else 'second'), 'rb') as f:
            self.estimations = pickle.load(f)