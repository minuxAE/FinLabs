"""
Greeks用于衡量期权的价格敏感性, 即相对于标的资产参数的变化

Delta: 衡量期权价格相对于标的资产价格的敏感性
Gamma: Delta相对于标的价格的变化率
"""

from BinomialLROption import BinomialLROption
import numpy as np

class BinomialLRWithGreeks(BinomialLROption):
    def __new_stock_price_tree__(self):
        # create additional layer of nodes to our original stock price tree
        self.STs = [np.array([self.S0 * self.u / self.d, self.S0, self.S0*self.d/self.u])]

        for i in range(self.N):
            prev_branches = self.STs[-1]
            st = np.concatenate((prev_branches * self.u, [prev_branches[-1] * self.d]))
            self.STs.append(st)

    def price(self):
        self._setup_parameters_()
        self.__new_stock_price_tree__()
        payoffs = self.__begin_tree_traversal__()

        option_value = payoffs[len(payoffs)//2]

        payoff_up = payoffs[0]
        payoff_down = payoffs[-1]

        S_up = self.STs[0][0]
        S_down = self.STs[0][-1]

        dS_up = S_up - self.S0
        dS_down = self.S0 - S_down

        # get delta value
        dS = S_up - S_down
        dV = payoff_up - payoff_down
        delta = dV / dS

        # get gamma value
        gamma = ((payoff_up - option_value) / dS_up - (option_value - payoff_down) / dS_down) / ((self.S0-S_up) / 2.0 - (self.S0+S_down)/2.0)

        return option_value, delta, gamma
    
"""
计算具有300个时间步长的欧式看涨期权和看跌期权价值、希腊值
"""
def main():
    eu_call = BinomialLRWithGreeks(50, 50, 0.05, 0.5, 300, {'sigma':0.3, 'is_call':True})
    res_call = eu_call.price()
    print('European call values')
    print('Price: {:.4f}'.format(res_call[0]))
    print('Delta: {:.4f}'.format(res_call[1]))
    print('Gamma: {:.4f}'.format(res_call[2]))

    eu_put = BinomialLRWithGreeks(50, 50, 0.05, 0.5, 300, {'sigma':0.3, 'is_call': False})
    res_put = eu_put.price()

    print('European put values')
    print('Price: {:.4f}'.format(res_put[0]))
    print('Delta: {:.4f}'.format(res_put[1]))
    print('Gamma: {:.4f}'.format(res_put[2]))

if __name__ == '__main__':
    main()

