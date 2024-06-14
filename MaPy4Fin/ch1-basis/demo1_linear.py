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

"""
PuLP求解线性规划问题

max 3x+2y
s.t. 2x+y <= 100
     x+y <= 80
     x <= 40
     x >= 0
     y >= 0
"""
import pulp

def Linear_Solver():
    x = pulp.LpVariable('x', lowBound=0)
    y = pulp.LpVariable('y', lowBound=0)

    prob = pulp.LpProblem('Maximization Problem', pulp.LpMaximize)
    prob += 3*x + 2*y, 'Objective Function'
    prob += 2*x + y <= 100, '1st constraint'
    prob += x + y <= 80, '2nd constraint'
    prob += x <= 40, '3rd constraint'
    prob.solve()

    for var in prob.variables():
        print(var.name, '=', var.varValue) 

import pulp

def IP_Solve1():
    dealers = ['X', 'Y', 'Z']
    variable_costs = {
        'X': 500,
        'Y': 350,
        'Z': 450
    }

    fixed_costs = {
        'X': 4000,
        'Y': 2000,
        'Z': 6000
    }

    quantities = pulp.LpVariable.dicts(
        'quantity',
        dealers,
        lowBound=0,
        cat=pulp.LpInteger
    )

    is_orders = pulp.LpVariable.dicts(
        'orders',
        dealers,
        cat = pulp.LpBinary
    )

    model = pulp.LpProblem('A cost minimization problem', pulp.LpMinimize)
    model += sum([(variable_costs[i] * quantities[i] + fixed_costs[i]) * is_orders[i] for i in dealers]), "Minimize Portfolio Cost"
    model += sum([quantities[i] for i in dealers]) == 150, "Total Contracts Required"
    model += 30 <= quantities['X'] <= 100, "Boundary of total Volume of X"
    model += 30 <= quantities['Y'] <= 90, "Boundary of total Volume of Y"
    model += 30 <= quantities['Z'] <= 70, "Boundary of total Volume of Z"

    model.solve() # 会执行非线性规划


def IP_Solve2():
    dealers = ['X', 'Y', 'Z']
    variable_costs = {
        'X': 500,
        'Y': 350,
        'Z': 450
    }

    fixed_costs = {
        'X': 4000,
        'Y': 2000,
        'Z': 6000
    }

    quantities = pulp.LpVariable.dicts(
        'quantity',
        dealers,
        lowBound=0,
        cat=pulp.LpInteger
    )

    is_orders = pulp.LpVariable.dicts(
        'orders',
        dealers,
        cat = pulp.LpBinary
    )

    model = pulp.LpProblem('A cost minimization problem', pulp.LpMinimize)
    
    # model += sum([(variable_costs[i] * quantities[i] + fixed_costs[i]) * is_orders[i] for i in dealers]), "Minimize Portfolio Cost"
    # 将所有未知变量以线性方式递增
    model += sum([variable_costs[i] * quantities[i] + fixed_costs[i] * is_orders[i] for i in dealers]), 'Minimize Portfolio Cost'

    model += sum([quantities[i] for i in dealers]) == 150, "Total Contracts Required"
    model += is_orders['X'] * 30 <= quantities['X'] <= is_orders['X'] * 100, "Boundary of total Volume of X"
    model += is_orders['Y'] * 30 <= quantities['Y'] <= is_orders['Y'] * 90, "Boundary of total Volume of Y"
    model += is_orders['Z'] * 30 <= quantities['Z'] <= is_orders['Z'] * 70, "Boundary of total Volume of Z"

    model.solve()

    for var in model.variables():
        print(var, '=', var.varValue)

    print('Total Cost is: ', pulp.value(model.objective))

"""
矩阵分解求解线性方程组
    2a + b + c = 4
    a + 3b + 2c = 5
    a = 6
"""
def Matrix_Solve():
    A = np.array([
        [2, 1, 1],
        [1, 3, 2],
        [1, 0, 0]
    ])

    B = np.array([4, 5, 6])
    print(np.linalg.solve(A, B)) # [6, 15, -23]

"""
LU分解: A=LU
"""
import scipy.linalg as linalg

def LU_Solve():
    A = np.array([
        [2, 1, 1],
        [1, 3, 2],
        [1, 0, 0]
    ])

    B = np.array([4, 5, 6])

    LU = linalg.lu_factor(A)
    x = linalg.lu_solve(LU, B)

    print(x)

"""
Cholesky分解
分解需要矩阵为实值对称矩阵
"""

def Cholesky_Solve():
    A = np.array([
        [10, -1, 2, 0],
        [-1, 11, -1, 3],
        [2, -1, 10, -1],
        [0, 3, -1, 8]
    ])

    B = np.array([6, 25, -11, 15])

    L = np.linalg.cholesky(A)

    print(L)

    print(np.dot(L, L.T.conj()))
    # Ax = B -> LL.Tx = B -> y = L.Tx
    y = np.linalg.solve(L, B)
    x = np.linalg.solve(L.T.conj(), y)
    print(x)

"""
QR分解
用于处理Ax=B的方程, A=QR, Q为正交矩阵, R为上三角矩阵
"""
def QR_Solve():
    A = np.array([
        [2, 1, 1],
        [1, 3, 2],
        [1, 0, 0]
    ])

    B = np.array([4, 5, 6])

    Q, R = linalg.qr(A) # QR decomposition
    y = np.dot(Q.T, B) # y = Q'B
    x = linalg.solve(R, y) # solve Rx = y
    print(x)

"""
其他矩阵代数方法
1. Jacobi迭代: 通过对矩阵对角元素迭代求解线性方程组, 计算结果收敛时终止迭代
如果矩阵A是一个不可约严格对角占优矩阵, 通过jacobi迭代得到的解一定是收敛的

不可约严格对角占优矩阵是每个对角元的绝对值都大于所在非对角元绝对值之和的矩阵

求解Ax=B, A=D+R
(D+R)x = B
Dx = B - Rx
x(n+1) = D^{-1}(B-Rx)
"""

def jacobi(A, B, n, tol=1e-10):
    x = np.zeros_like(B) # initialize

    for it_count in range(n):
        x_new = np.zeros_like(x)
        for i in range(A.shape[0]):
            s1 = np.dot(A[i, :i], x[:i])
            s2 = np.dot(A[i, i+1:], x[i+1:])
            x_new[i] = (B[i] - s1 - s2) / A[i, i]
        
        if np.allclose(x, x_new, tol):
            break

        x = x_new
    return x

def Jacobi_Solve():
    A = np.array([
    [10., -1., 2., 0.], 
    [-1., 11., -1., 3.], 
    [2., -1., 10., -1.], 
    [0.0, 3., -1., 8.]])

    # B = np.array([6, 25, -11, 15]) # 这里存在精度问题
    B = np.array([6., 25., -11., 15.])
    n = 25

    x = jacobi(A, B, n)
    print(x)    

"""
2. Gauss-Seidel迭代法
Ax = B
(L+U)x = B
Lx = B - Ux
x(n+1) = L^{-1}(B-Ux(n))
"""
def gauss(A, B, n, tol=1e-10):
    L = np.tril(A) # returns the lower triangle matrix of A
    U = A - L
    L_inv = np.linalg.inv(L)
    x = np.zeros_like(B)

    for i in range(n):
        Ux = np.dot(U, x)
        x_new = np.dot(L_inv, B-Ux)

        if np.allclose(x, x_new, tol):
            break

        x = x_new

    return x

def Gauss_Solve():
    A = np.array([
        [10, -1, 2, 0],
        [-1, 11, -1, 3],
        [2, -1, 10, -1],
        [0, 3, -1, 8]
    ])

    B = np.array([6, 25, -11, 15])

    n = 100

    x = gauss(A, B, n)
    print(x)    

if __name__ == '__main__':
    # Gauss_Solve()
    Jacobi_Solve()
    # QR_Solve()
    # Cholesky_Solve()
    # LU_Solve()
    # Matrix_Solve()
    # IP_Solve2()
    # Linear_Solver()
    # Beta_Regress()
    # APT_Regress()


