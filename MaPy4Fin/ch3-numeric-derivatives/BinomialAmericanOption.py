"""
美式期权可以在到期日前任何时间行权

_initialize_stock_price_tree_: 使用二维数组存储所有时间步长股票价格的预期收益，用于计算每个期间的行权收益
_initialize_payoffs_tree_: 将收益树创建为二维数组, 以期权到期时间的内在价值为起点
__check_early_exercise__: 私有方法, 可以在提前行权与不行权之间返回最大收益值
_traverse_tree_: 该方法调用__check_early_exercise__方法以检查在任意时间步长中提前行权可获得的最佳收益
"""
from StockOption import StockOption
import math
import numpy as np

class BinomialTreeOption(StockOption):
    def _setup_parameters_(self):
        self.u = 1+self.pu # expected value in the up state
        self.d = 1-self.pd # expected value in the down state
        self.qu = (math.exp((self.r - self.div) * self.dt) - self.d) / (self.u - self.d)
        self.qd = 1 - self.qu

    def _initialize_stock_price_tree(self):
        # initialize a 2D Tree at T=0
        self.STs = [np.array([self.S0])]

        # simulate possible stock prices path
        for i in range(self.N):
            prev_branches = self.STs[-1]
            st = np.concatenate((prev_branches * self.u, [prev_branches[-1] * self.d]))
            self.STs.append(st) # add nodes at each time step

    def _initialize_payoffs_tree_(self):
        # the payoffs when option expires
        return np.maximum(
            0, (self.STs[self.N] - self.K) if self.is_call
            else (self.K - self.STs[self.N])
        )
    
    def __check_early_exercise__(self, payoffs, node):
        early_ex_payoff = (self.STs[node] - self.K) if self.is_call else (self.K - self.STs[node])
        return np.maximum(payoffs, early_ex_payoff)
    
    def _traverse_tree_(self, payoffs):
        for i in reversed(range(self.N)):
            # Payoffs from NOT exercising the option
            payoffs = (payoffs[:-1] * self.qu + payoffs[1:] * self.qd) * self.df

            # Payoffs from exercising, for American options
            if not self.is_european:
                payoffs = self.__check_early_exercise__(payoffs, i)
        return payoffs
    
    def __begin_tree_traversal__(self):
        payoffs = self._initialize_payoffs_tree_()
        return self._traverse_tree_(payoffs)
    
    def price(self):
        self._setup_parameters_()
        self._initialize_stock_price_tree()
        payoffs = self.__begin_tree_traversal__()

        return payoffs[0]

"""
美式期权可以在到期日前的任意时间点行权, 欧式期权只能在到期行权
美式期权的灵活性, 使得其价值不低于对等的欧式期权的价值

如果美式看涨期权的标的资产为不支付股息的股票, 其对欧式看涨期权可能没有额外的价值。
根据货币的时间价值理论, 期权到期行权比以相同行权价格在未来某个时间行权收益更小. 对于不分配股息的实值看涨期权, 期权持有人没有提前行权的动机.
"""

def main():
    params = {'pu': 0.2, 'pd': 0.2, 'is_call': False, 'is_eu': False}
    am_option = BinomialTreeOption(50, 50, 0.05, 0.5, 2, params)
    print(am_option.price())

if __name__ == '__main__':
    main()
    

        