
from chapter01.get_all_states import all_states
from chapter01.state import State
import warnings
warnings.filterwarnings("ignore")

# 裁决器
# 先手player1（用 -1 表示）， 后手player2（用 1 表示）
class Judger:
    def __init__(self, player1, player2):
        self.p1 = player1
        self.p2 = player2
        self.current_player = None
        self.p1_symbol = 1       # 先手玩家标志
        self.p2_symbol = -1      # 后手玩家标志
        self.p1.set_symbol(self.p1_symbol)
        self.p2.set_symbol(self.p2_symbol)
        self.current_state = State()

    def reset(self):
        self.p1.reset()
        self.p2.reset()

    def alternate(self):
        while True:
            yield self.p1
            yield self.p2

    # @print_state: if True, 打印游戏中的每个棋盘
    def play(self, print_state=False):
        alternator = self.alternate()
        self.reset()
        current_state = State()
        self.p1.set_state(current_state)
        self.p2.set_state(current_state)
        if print_state:
            current_state.print_state()
        while True:
            # 返回一个iterator对象
            player = next(alternator)
            # 棋手所下的位置以及 先后手的标志symbol
            i, j, symbol = player.act()
            # 下一个状态的哈希值
            next_state_hash = current_state.next_state(i, j, symbol).hash()
            current_state, is_end = all_states[next_state_hash]
            self.p1.set_state(current_state)
            self.p2.set_state(current_state)
            if print_state:
                current_state.print_state()
            # 游戏结束， 打印当前状态 赢家是谁。
            if is_end:
                return current_state.winner
