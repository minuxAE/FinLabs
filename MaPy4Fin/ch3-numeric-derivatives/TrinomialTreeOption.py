from BinomialAmericanOption import BinomialTreeOption
import math
import numpy as np

"""
三叉树模型定价
"""

class TrinomialTreeOption(BinomialTreeOption):

    def _setup_parameters_(self):
        self.u = math.exp(self.sigma*math.sqrt(2*self.dt))
        self.d = 1 / self.u
        self.m = 1
        self.qu = ((math.exp((self.r-self.div) * self.dt / 2.) - 
                    math.exp(-self.sigma * math.sqrt(self.dt / 2.))) / 
                    (math.exp(self.sigma * math.sqrt(self.dt /2.)) - 
                     math.exp(-self.sigma * math.sqrt(self.dt / 2.)))) ** 2
        
        self.qd = ((math.exp(self.sigma * math.sqrt(self.dt/2.)) - 
                    math.exp((self.r - self.div) * self.dt/2.)) / (math.exp(self.sigma*math.sqrt(self.dt/2)) - 
                                                                   math.exp(-self.sigma * math.sqrt(self.dt/2.)))) ** 2
        
        self.qm = 1 - self.qu - self.qd

    
    def _initialize_stock_price_tree(self):
        # initialize a 2D tree at t=0
        self.STs = [np.array([self.S0])]

        for i in range(self.N):
            prev_nodes = self.STs[-1]
            self.ST = np.concatenate(
                (prev_nodes * self.u, [prev_nodes[-1] * self.m, prev_nodes[-1] * self.d])
            )

            self.STs.append(self.ST)

    def _traverse_tree_(self, payoffs):
        for i in reversed(range(self.N)):
            payoffs = (payoffs[:-2] * self.qu + payoffs[1:-1] * self.qm + payoffs[2:] * self.qd) * self.df

            if not self.is_european:
                payoffs = self.__check_early_exercise__(payoffs, i)

        return payoffs

def main():
    eu_put = TrinomialTreeOption(50, 50, 0.05, 0.5, 2, {'sigma': 0.3, 'is_call': False})
    print('European put is {:.4f}'.format(eu_put.price()))
    am_option = TrinomialTreeOption(50, 50, 0.05, 0.5, 2, {'sigma': 0.3, 'is_call': False, 'is_eu': False})
    print('American put is {:.4f}'.format(am_option.price()))


if __name__ == '__main__':
    main()
