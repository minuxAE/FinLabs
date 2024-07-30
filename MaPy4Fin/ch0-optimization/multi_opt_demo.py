"""
工厂需要将N份工作分配给N个工人, 每份工作只能由1个人做, 每个工人也只能做一份工作, 假设工人i处理工作j需要时间
Tij, 获得的利润是Cij, 如何安排才能使得总利润最大且总耗时最小.

主要目标: 利润最大化
次要目标：耗时最小化
"""

import gurobipy as grb
import numpy as np

N = 10 # 设定工人数和工作数量
np.random.seed(2024)

# 使用随机数初始化时间矩阵Tij和成本矩阵Cij

Tij = {(i+1, j+1): np.random.randint(0, 100) for i in range(N) for j in range(N)}
Cij = {(i+1, j+1): np.random.randint(0, 100) for i in range(N) for j in range(N)}

m = grb.Model('MultiObj')

# x是0-1变量类型, xij=1表示第i个工人被分配到第j个工作中
x = m.addVars(Tij.keys(), vtype=grb.GRB.BINARY, name='x')

# 添加约束
# 约束1：一份工作只能分配给一个工人
m.addConstrs((x.sum('*', j+1) == 1 for j in range(N)), 'C1')
# 约束2：一个工人只能做一份工作
m.addConstrs((x.sum(i+1, '*') == 1 for i in range(N)), 'C2')

# 多目标方式1：Blend合成
# 设置多目标权重
# x.prod(Tij) # 工人分配矩阵Xij和时间矩阵Tij通过相同的索引进行相乘

# 设定优化目标
# m.setObjectiveN(x.prod(Tij), index=0, weight=0.1, name='obj1')
# m.setObjectiveN(-x.prod(Cij), index=1, weight=0.5, name='obj2')

# 多目标方式2：Hierchical分层
m.setObjectiveN(x.prod(Tij), index=0, priority=1, abstol=0, reltol=0, name='obj1')
m.setObjectiveN(-x.prod(Cij), index=1, priority=2, abstol=100, reltol=0, name='obj2')


m.optimize()

# 获得求解结果
for i in Tij.keys():
    if x[i].x > 0.9:
        print('Worker {} assigned {}'.format(i[0], i[1]))

# 获取目标函数值
for i in range(2):
    m.setParam(grb.GRB.Param.ObjNumber, i)
    print('Obj{} = {}'.format(i+1, m.ObjNVal))




