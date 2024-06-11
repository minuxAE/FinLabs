"""
1.CAPM模型, Efficient Frontier, CML
2.使用回归方程求解SML
3.APT和多元线性回归
4.Portfolio
5.PuLP线性优化
6.线性规划的结果
7.整数规划
8.矩阵求解线性方程组
9.Jacobi迭代和Gauss-Seidel迭代
"""
from scipy import stats
import numpy as np
import statsmodels.api as sm
"""
Capital Market Line, CML. 所有最优投资组合中Sharpe ratio最高的那个
Security Market Line, SML. 资产对于Beta系数的期望收益
"""
def Beta_Regress():
    stock_returns = [0.065, 0.0265, -0.0593, -0.001, 0.0346]
    mkt_returns = [0.055, -0.09, -0.041, 0.045, 0.022]

    beta, alpha, r_value, p_value, std_err = stats.linregress(stock_returns, mkt_returns)
    print('Beta is {:.4f}, Alpha is {:.4f}'.format(beta, alpha))


def APT_Regress():
    num_periods = 9
    all_values = np.array([np.random.random(8) for _ in range(num_periods)])

    # Filter Data
    y_values = all_values[:, 0]
    x_values = all_values[:, 1:]

    x_values = sm.add_constant(x_values)
    res = sm.OLS(y_values, x_values).fit()
    print(res.summary())

if __name__ == '__main__':
    # Beta_Regress()
    APT_Regress()


