"""
类似于Lagrangian松弛法, 可以将线性规划问题表示为如下函数:

min f(x) = c^Tx + sum I (Ax-b)

考虑到indicator function不可导, 考虑使用替代函数 I=-1/t * log(-u)

对应转换形式如下:

min f(x) = tc^Tx - sum log(-Ax + b)
"""
from sympy import diff, symbols, exp, log

# 定义变量
x1, x2, t = symbols('x1 x2 t')

# 定义目标函数
func = t*(-70*x1-30*x2) - log(-3*x1-9*x2+540) - log(-5*x1-5*x2+450) - log(-9*x1-3*x2+720) - log(x1) - log(-x2)

# 求导
diff(func, x1, 1) # 对x1求一阶导数
diff(func, x2, 1) # 对x2求一阶导数
diff(func, x1, x1) # 对x1和x1求二阶导数
diff(func, x1, x2) # 对x1和x2求二阶导数
diff(func, x2, x1) # 对x2和x1求二阶导数
diff(func, x2, x2) # 对x2和x2求二阶导数

"""
内点法

原问题转为无约束优化为:

"""
import numpy as np
import time

def gradient(x1, x2, t):
    # 计算梯度函数
    j1 = -70 * t + 3 / (-3 * x1 - 9 * x2 + 540) + 5 / (-5 * x1 - 5 * x2 + 450) + 9 / (-9 * x1 - 3 * x2 + 720) - 1 / x1
    j2 = -30 * t + 9 / (-3 * x1 - 9 * x2 + 540) + 5 / (-5 * x1 - 5 * x2 + 450) + 3 / (-9 * x1 - 3 * x2 + 720) - 1 / x2
    return np.asmatrix([j1, j2]).T

def hessian(x1, x2):
    # 计算Hessian矩阵
    x1, x2 = float(x1), float(x2)
    h11 = 9 / (3 * x1 + x2 - 240) ** 2 + (x1 + 3 * x2 - 180) ** (-2) + (x1 + x2 - 90) ** (-2) + x1 ** (-2)
    h12 = 3 / (3 * x1 + x2 - 240) ** 2 + 3 / (x1 + 3 * x2 - 180) ** 2 + (x1 + x2 - 90) ** (-2)
    h21 = 3 / (3 * x1 + x2 - 240) ** 2 + 3 / (x1 + 3 * x2 - 180) ** 2 + (x1 + x2 - 90) ** (-2)
    h22 = (3 * x1 + x2 - 240) ** (-2) + 9 / (x1 + 3 * x2 - 180) ** 2 + (x1 + x2 - 90) ** (-2) + x2 ** (-2)
    return np.asmatrix([[h11, h12], [h21, h22]])

def invertible(H):
    return np.linalg.inv(H)

def main():
    x = np.asmatrix(np.array([10, 10])).T # 设定迭代初始值
    t = 0.00001 # 指示函数
    eps = 0.01 # 迭代误差
    iter_cnt = 0 # 记录迭代次数

    while iter_cnt < 20:
        iter_cnt += 1
        J = gradient(x[0, 0], x[1, 0], t)
        H = hessian(x[0, 0], x[1, 0])
        Hinv = np.linalg.inv(H)
        x_new = x - Hinv * J
        err = np.linalg.norm(x_new - x)
        print('Iteration {} x1 = {:.4f}, x2 = {:.4f}, error = {:.4f}'.format(iter_cnt, x_new[0, 0], x_new[1, 0], err))

        x = x_new
        if err < eps:
            break
        time.sleep(0.2)

    print('Objective function value is {:.4f}'.format(70 * x[0, 0] + 30 * x[1, 0]))


if __name__ == '__main__':
    main()

