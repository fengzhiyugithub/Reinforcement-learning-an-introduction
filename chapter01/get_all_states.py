
from chapter01.state import State
from chapter01.common import *

# 获取棋盘的所有可能的状态
def get_all_states_impl(current_state, current_symbol, all_states):
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            # 若当前状态还有棋点为 空（双方都没有下），则更新状态
            if current_state.data[i][j] == 0:
                new_state = current_state.next_state(i, j, current_symbol)
                new_hash = new_state.hash()
                if new_hash not in all_states:
                    is_end = new_state.is_end()
                    all_states[new_hash] = (new_state, is_end)
                    # 若游戏未结束（is_end == False）
                    if not is_end:
                        get_all_states_impl(new_state, -current_symbol, all_states)


def get_all_states():
    current_symbol = 1
    current_state = State()
    # 棋盘状态（current_state, is_end）由当前状态和游戏结束标志组成
    all_states = dict()
    all_states[current_state.hash()] = (current_state, current_state.is_end())
    get_all_states_impl(current_state, current_symbol, all_states)
    return all_states


# 所有可能的棋盘状态
all_states = get_all_states()



