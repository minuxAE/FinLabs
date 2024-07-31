"""
单纯形法求解线性规划问题
"""

import numpy as np
import pandas as pd
from pandas import DataFrame

def lp_solver(matrix:DataFrame):
    """
    max cx
    s.t. ax <= b

    矩阵形式
            b   x1  x2  x3  x4  x5
    obj     0   70  30  0   0   0
    x3      540 3   9   1   0   0
    x4      450 5   5   0   1   0
    x5      720 9   3   0   0   1

    第1行, 目标函数得系数
    2-4行, 约束方程得系数
    第1列, 约束方程得常数项
    obj-b交叉, 目标函数的负值
    """
    # 查看检验数是否为正
    c = matrix.iloc[0, 1:]
    while c.max() > 0:
        # 换基, 选择入基变量, 目标函数系数最大的变量入基
        c = matrix.iloc[0, 1:]
        in_x = c.idxmax() # 入基变量的索引
        in_x_v = c[in_x] # 入基变量的系数

        # 选择出基变量
        # min(b/ai) 选择正的最小比值对应的变量出基
        b = matrix.iloc[1:, 0] # 非基变量的系数ai
        in_x_a = matrix.iloc[1:][in_x] # 入基变量对应的ai
        out_x = (b / in_x_a).idxmin() # 计算 b / ai, 得到出基变量

        # 旋转单纯形表
        matrix.loc[out_x, :] = matrix.loc[out_x, :] / matrix.loc[out_x, in_x]
        # 进行Gauss消元
        for idx in matrix.index:
            if idx != out_x:
                matrix.loc[idx, :] = matrix.loc[idx, :] - matrix.loc[out_x, :] * matrix.loc[idx, in_x]

        # 索引替换（替换入基和出基变量名称）
        index = matrix.index.tolist()
        i = index.index(out_x)
        index[i] = in_x
        matrix.index = index

    print('The final Simplex Table is:\n')
    print(matrix)
    print('Objective function value is: {}'.format(-matrix.iloc[0, 0]))
    print('Optimal decision variables are: ')
    x_count = (matrix.shape[1] - 1) - (matrix.shape[0] - 1)
    X = matrix.iloc[0, 1:].index.tolist()[:x_count]

    for xi in X:
        print(xi, '=', matrix.loc[xi, 'b'])

# 主程序代码
"""
求解问题

max Z = 70x1 + 30x2

s.t.
    3x1 + 9x2 + x3 = 540
    5x1 + 5x2 + x4 = 450
    9x1 + 3x2 + x5 = 720
    x1, x2, x3, x4, x5 >= 0
"""


def main():
    # 约束方程系数矩阵，包含常数项
    matrix = pd.DataFrame(
        np.array([
            [0, 70, 30, 0, 0, 0],
            [540, 3, 9, 1, 0, 0],
            [450, 5, 5, 0, 1, 0],
            [720, 9, 3, 0, 0, 1]]),
        index=['obj', 'x3', 'x4', 'x5'],
        columns=['b', 'x1', 'x2', 'x3', 'x4', 'x5'])

    # 调用前面定义的函数求解
    lp_solver(matrix)

    

if __name__ == '__main__':
    main()