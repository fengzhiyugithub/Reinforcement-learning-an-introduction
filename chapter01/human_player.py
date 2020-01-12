from chapter01.common import *
import warnings
warnings.filterwarnings("ignore")

'''
 人类玩家接口
 输入一个字符，如下
 | q | w | e |
 | a | s | d |
 | z | x | c |
'''


class HumanPlayer:
    # **kwargs 当传入参数为dict()类型时使用
    def __init__(self, **kwargs):
        self.symbol = None
        self.keys = ['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c']
        self.state = None

    def reset(self):
        pass

    def set_state(self, state):
        self.state = state

    def set_symbol(self, symbol):
        self.symbol = symbol

    # 下棋
    def act(self):
        self.state.print_state()
        key = input("Input your position:")
        data = self.keys.index(key)
        i = data // BOARD_COLS
        j = data % BOARD_COLS
        return i, j, self.symbol
