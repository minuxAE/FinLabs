"""
Leisen-Reimer模型

通过步数的增加得到接近BS模型的解, 使用反演公式得到更加准确的解
"""
from BinomialAmericanOption import BinomialTreeOption
import math

class BinomialLROption(BinomialTreeOption):
    def _setup_parameters_(self):
        odd_N = self.N if (self.N%2 == 1) else (self.N+1)
        d1 = (math.log(self.S0 / self.K) + ((self.r - self.div) + (self.sigma**2)/2) * self.T) / (self.sigma * math.sqrt(self.T))
        d2 = (math.log(self.S0 / self.K) + ((self.r - self.div) - (self.sigma**2)/2) * self.T) / (self.sigma * math.sqrt(self.T))

        pp2_inversion = lambda z, n: 0.5+math.copysign(1, z) * math.sqrt(0.25 - 0.25*math.exp(-((z/(n+1/3+1/(n+1)))**2)*(n+1/6)))
        pbar = pp2_inversion(d1, odd_N)

        self.p = pp2_inversion(d2, odd_N)
        self.u = 1 / self.df * pbar / self.p
        self.d = (1 / self.df - self.p * self.u) / (1-self.p)
        self.qu = self.p
        self.qd = 1-self.p


def main():
    params1 = {'sigma': 0.3, 'is_call': False}
    eu_option = BinomialLROption(50, 50, 0.05, 0.5, 3, params1)
    print('LR: European Put Option is ', eu_option.price())

    params2 = {'sigma': 0.3, 'is_call': False, 'is_eu': False}
    am_option = BinomialLROption(50, 50, 0.05, 0.5, 3, params2)
    print('LR: American Put Option is ', am_option.price())

if __name__ == '__main__':
    main()

