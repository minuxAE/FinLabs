"""
Binomial European Option
"""
from StockOption import StockOption
import math
import numpy as np

class BinomialEuropeanOption(StockOption):
    def __setup_parameters_(self):
        # Required calculations for the model
        self.M = self.N + 1 # number of terminal nodes of tree
        self.u = 1 + self.pu # expected value in the up state
        self.d = 1 - self.pd # expected value in the down state
        self.qu = (math.exp((self.r - self.div) * self.dt) - self.d) / (self.u - self.d)
        self.qd = 1-self.qu

    def _initialize_stock_price_tree_(self):
        # Initialize terminal price nodes to zeros
        self.STs = np.zeros(self.M) # 末端节点初始化

        # calculate expected stock prices for each node
        for i in range(self.M): # 股价期望计算
            self.STs[i] = self.S0*(self.u**(self.N-i))*(self.d**i)

    def _initialize_payoffs_tree_(self):
        # Get payoffs when the option expires at terminal nodes
        payoffs = np.maximum(
            0, (self.STs - self.K) if self.is_call
            else (self.K - self.STs)
        )

        return payoffs
    
    def _traverse_tree_(self, payoffs):
        # 逆向计算, starting from the time the option expires, traverse
        # backwards and calculate discounted payoffs at each node
        for i in range(self.N):
            payoffs = (payoffs[:-1] * self.qu + payoffs[1:] * self.qd) * self.df
        return payoffs

    def __begin_tree_traversal_(self):
        payoffs = self._initialize_payoffs_tree_()
        return self._traverse_tree_(payoffs)

    def price(self):
        # pricing implementation
        self.__setup_parameters_()
        self._initialize_stock_price_tree_()
        payoffs = self.__begin_tree_traversal_()

        return payoffs[0]


def main():
    params = {'pu': 0.2, 'pd': 0.2, 'is_call': False}
    eu_option = BinomialEuropeanOption(50, 50, 0.05, 0.5, 2, params)
    print(eu_option.price())

if __name__ == '__main__':
    main() 