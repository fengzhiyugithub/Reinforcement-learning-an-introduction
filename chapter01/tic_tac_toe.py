#######################################################################
# Copyright (C)                                                       #
# 2016-2018 Shangtong Zhang(zhangshangtong.cpp@gmail.com)             #
# 2016 Tian Jun(tianjun.cpp@gmail.com)                                #
# 2016 Artem Oboturov(oboturov@gmail.com)                             #
# 2016 Kenta Shimada(hyperkentakun@gmail.com)                         #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################

import warnings
from chapter01 import human_player as hp
from chapter01.AI import Player
from chapter01.judger import Judger

warnings.filterwarnings("ignore")

'''
    function: RL训练模型使用使用最优策略判定谁为胜方或平局。
    goal：    3*3大小的田字格，连成3个连续字符是同一个符号的为胜方。
'''

# 训练模型, 训练回合数epochs
def train(epochs, print_every_n=500):
    player1 = Player(epsilon=0.01)
    player2 = Player(epsilon=0.01)
    judger = Judger(player1, player2)
    player1_win = 0.0
    player2_win = 0.0
    for i in range(1, epochs + 1):
        # 无打印状态获取 当前
        winner = judger.play(print_state=False)
        if winner == 1:
            player1_win += 1
        if winner == -1:
            player2_win += 1
        if i % print_every_n == 0:
            print('Epoch %d, player 1 winrate:%.02f, player 2 winrate: %.02f' % (i, player1_win / i, player2_win / i))
        # 更新玩家的值估计
        player1.backup()
        player2.backup()
        judger.reset()
    # 保存玩家1，2的最优策略
    player1.save_policy()
    player2.save_policy()


# 模型测试
def compete(turns):
    player1 = Player(epsilon=0)
    player2 = Player(epsilon=0)
    judger = Judger(player1, player2)
    # 加载两个玩家的最优策略
    player1.load_policy()
    player2.load_policy()
    player1_win = 0.0
    player2_win = 0.0
    for _ in range(turns):
        winner = judger.play()
        if winner == 1:
            player1_win += 1
        if winner == -1:
            player2_win += 1
        judger.reset()
    print('%d turns, player 1 win %.02f, player 2 win %.02f' % (turns, player1_win / turns, player2_win / turns))


# 如果人类玩家采取最优策略， 游戏将是平局
def play():
    while True:
        # 人类玩家先手
        player1 = hp.HumanPlayer()
        player2 = Player(epsilon=0)
        judger = Judger(player1, player2)
        # AI玩家（后手）采用最优策略
        player2.load_policy()
        # 获取裁决器判决当前状态的胜方
        winner = judger.play()
        if winner == player2.symbol:
            print('You lose!')
        elif winner == player1.symbol:
            print('You win!')
        else:
            print("It is a tie!")

# 如果下棋双方都采取最优策略， 将一直会是平局
if __name__ == "__main__":
    # 模型训练， 获取井字棋所有可能的状态并保存最优策略
    train(int(1e5))
    # 模型测试
    compete(int(1e3))
    # 玩家（先手）与 AI 下棋
    play()
