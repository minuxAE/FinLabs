"""
Cox-Ross-Rubinstein模型

CRR模型提出 短期风险中性环境下二项模型中标的股票的均值和方差
"""
from BinomialAmericanOption import BinomialTreeOption
import math

class BinomialCRROption(BinomialTreeOption):
    def _setup_parameters_(self):
        self.u = math.exp(self.sigma * math.sqrt(self.dt))
        self.d = 1 / self.u
        self.qu = (math.exp((self.r-self.div) * self.dt) - self.d) / (self.u-self.d)
        self.qd = 1 - self.qu

def main():
    params1 = {'sigma': 0.3, 'is_call': False}
    eu_option = BinomialCRROption(50, 50, 0.05, 0.5, 2, params1)

    print('CRRO: European Put Option: ', eu_option.price())

    params2 = {'sigma': 0.3, 'is_call': False, 'is_eu': False}
    am_option = BinomialCRROption(50, 50, 0.05, 0.5, 2, params2)

    print('CRRO: American Put Option: ', am_option.price())

if __name__ == '__main__':
    main()