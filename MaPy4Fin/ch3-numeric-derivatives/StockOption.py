"""
使用数值方法进行衍生品定价

1. Lattice方法在每个步骤仅存储新信息, 并重用已经存储的值解决问题
2. 有限差分方法中，树的结点可以表示网格
"""
import math
"""
Stock Option类: 存储股票期权的通用属性
"""
class StockOption(object):
    def __init__(self, S0, K, r, T, N, params) -> None:
        self.S0 = S0
        self.K = K
        self.r = r
        self.T = T
        self.N = max(1, N)
        self.STs = None # stock prices tree

        # optioal parameters by the derived classes
        self.pu = params.get('pu', 0) # probability of up state
        self.pd = params.get('pd', 0) # probability of down state
        self.div = params.get('div', 0) # dividend yield
        self.sigma = params.get('sigma', 0) # volatility
        self.is_call = params.get('is_call', True) # Call or Put
        self.is_european = params.get('is_eu', True) # Eu or Am

        self.dt = T / float(N)
        self.df = math.exp(-(r-self.div) * self.dt) # discount factor
        